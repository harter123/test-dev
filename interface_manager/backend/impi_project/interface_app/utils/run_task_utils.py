import json
import jsonpath
from interface_app.models.result import TaskResult, InterfaceResult
from interface_app.models.task import Task, TASK_STATUS, TaskInterface
from interface_app.utils.task_utils import TaskUtils
from interface_app.models.interface import Interface
from interface_app.utils.interface_utils import InterfaceUtils


class RunTaskUtils:
    """
    任务执行的主类
    """

    def __init__(self, task, args):
        self.task = task
        self.args = args

    def __update_task_status(self, status):
        """
        更新任务状态
        :param status:
        :return:
        """
        self.task.status = status
        self.task.save()

    def __get_task_interfaces(self):
        """
        获取任务所有的接口
        :return:
        """
        results = TaskInterface.objects.filter(task_id=self.task.id)
        ret = []
        for i in results:
            ret.append(i.interface)
        return ret

    def __run_interface(self, interface):
        """
        执行单个接口
        :param interface:
        :return:
        """
        if not interface or not isinstance(interface, Interface):
            return ""

        url = interface.url
        if "host" in self.args:
            url = self.args["host"] + "/" + url
        else:
            if interface.host:
                url = interface.host + "/" + url
        text = InterfaceUtils.send_request("http://" + url, interface.method, interface.header, interface.parameter,
                                           interface.parameter_type)
        return text

    def __save_interface_result(self, interface, success, response, version):
        """
        保存接口的历史数据
        :param interface:
        :param response:
        :param success:
        :param version:
        :return:
        """
        history = InterfaceResult()
        history.task_result_id = version.id
        history.interface_id = interface.id

        history.name = interface.name
        history.description = interface.description
        history.host = interface.host if not self.args.get("host", "") else self.args.get("host")
        history.url = interface.url
        history.method = interface.method
        history.header = interface.header
        history.parameter = interface.parameter
        history.parameter_type = interface.parameter_type

        if "text" == interface.response_type:
            history.response_type = "text"
            history.response = {"text": response}
        else:
            try:
                r = json.loads(response, encoding="utf-8")
                history.response_type = "json"
            except Exception:
                history.response_type = "text"
                r = {"text": response}
            history.response = r
        history.assertion = interface.assertion
        history.success = success
        history.save()

    def __save_task_result(self):
        """
        创建一个任务结果版本数据
        :return:
        """
        result = TaskUtils.get_last_result(self.task.id)
        if result is None:
            version = TaskResult.objects.create(task_id=self.task.id)
        else:
            version = TaskResult.objects.create(task_id=self.task.id, version=result.version + 1)
        return version

    def __assert_result(self, interface, response):
        """
        接口断言
        :param interface:
        :param response:
        :return:
        """
        if not interface or not isinstance(interface, Interface):
            return False
        if not response:
            return True

        for i in interface.assertion:
            result = True
            if "value" in i:
                result = self.__assert_json(response, i)
            else:
                result = self.__assert_text(response, i)
            if not result:
                return False
        return True

    def __assert_text(self, response, assertion):
        """
        文本断言
        :param response:
        :param assertion:
        :return:
        """
        key = assertion["key"]
        if key in response:
            return True if "yes" == assertion["include"] else False
        else:
            return False if "yes" == assertion["include"] else True

    def __assert_json(self, response, assertion):
        """
        json型的断言， 使用jsonPath的语法
        :param response:
        :param assertion:
        :return:
        """
        value = self.__parse_assert_value(assertion["type"], assertion["value"])
        try:
            obj = json.loads(response, encoding="utf-8")
            results = jsonpath.jsonpath(obj, assertion["key"])
            if not results:
                return False
            if value in results:
                return True if "yes" == assertion["include"] else False
            else:
                return False if "yes" == assertion["include"] else True
        except Exception:
            return False

    def __parse_assert_value(self, p_type, value):
        """
        把断言里面的数据进行数据转换
        :param p_type:
        :param value:
        :return:
        """
        try:
            if "string" == p_type:
                return str(value)
            elif "int" == p_type:
                return int(value)
            elif "float" == p_type:
                return float(value)
            elif "bool" == p_type:
                return bool(value)
            else:
                return value
        except Exception:
            return value

    def run(self):
        if not self.task or not isinstance(self.task, Task):
            return False
        if TASK_STATUS[1][0] == self.task.status:
            return False
        self.__update_task_status(TASK_STATUS[0][0])
        version = self.__save_task_result()
        interfaces = self.__get_task_interfaces()
        for i in interfaces:
            response = self.__run_interface(i)
            success = self.__assert_result(i, response)
            self.__save_interface_result(i, success, response, version)
        self.__update_task_status(TASK_STATUS[2][0])
