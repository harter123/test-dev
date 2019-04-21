import json
from interface_app import common
from interface_app.form.task import TaskForm
from interface_app.models.task import Task, TaskInterface
from interface_app.models.result import TaskResult

from django.views.generic import View
from interface_app.my_exception import MyException


# Create your views here.
# task的列表获取和创建的接口

class TaskListViews(View):
    def get(self, request, *args, **kwargs):
        """
        获取任务列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        results = Task.objects.all()
        ret = list()
        for i in results:
            tmp = dict()
            tmp["id"] = i.id
            tmp["name"] = i.name
            tmp["description"] = i.description
            tmp["status"] = i.get_status_display()  # 获取choice的描述
            tmp["interface_count"] = TaskInterface.objects.filter(task_id=i.id).count()
            tmp["result_count"] = TaskResult.objects.filter(task_id=i.id).count()
            ret.append(tmp)
        return common.response_success(ret)

    def post(self, request, *args, **kwargs):
        """
        创建任务
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        body = request.body
        params = json.loads(body)
        form = TaskForm(params)
        result = form.is_valid()
        if result:
            service = Task.objects.create(**form.cleaned_data)
            if service:
                return common.response_success()
            else:
                raise MyException("创建任务失败")
        else:
            print(form.errors.as_json())
            return common.response_failed()
