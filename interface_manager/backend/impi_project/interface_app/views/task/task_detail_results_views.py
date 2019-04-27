import datetime
from django.forms.models import model_to_dict
from interface_app import common
from interface_app.models.task import Task, TaskInterface
from interface_app.models.result import TaskResult, InterfaceResult

from django.views.generic import View
from interface_app.my_exception import MyException


# Create your views here.
# task的接口的增删改查

class TaskDetailVersionViews(View):
    def get(self, request, pk, *args, **kwargs):
        """
        获取单个任务的版本列表
        :param request:
        :param pk: # 任务的id
        :param args:
        :param kwargs:
        :return:
        """
        results = TaskResult.objects.filter(task_id=pk).order_by('-version')
        ret = []
        for i in results:
            tmp = dict()
            tmp["version"] = i.version
            tmp["task_id"] = i.task_id
            tmp['created'] = i.created.strftime("%Y-%m-%d %H:%M")
            ret.append(tmp)
        return common.response_success(ret)

class TaskDetailVersionResultsViews(View):
    def get(self, request, pk, *args, **kwargs):
        """
        获取一个版本的结果列表
        :param request:
        :param pk: # 任务的id
        :param args:
        :param kwargs:
        :return:
        """
        results = InterfaceResult.objects.filter(task_result_id=pk)
        ret = [model_to_dict(i) for i in results]
        return common.response_success(ret)
