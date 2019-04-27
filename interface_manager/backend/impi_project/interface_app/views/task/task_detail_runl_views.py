import json
from django.forms.models import model_to_dict
from interface_app import common
from interface_app.form.task import TaskForm
from interface_app.models.task import Task, TaskInterface
from interface_app.models.result import TaskResult

from django.views.generic import View
from interface_app.my_exception import MyException


# Create your views here.
# task的执行的接口

class TaskDetailRunViews(View):

    def post(self, request, pk, *args, **kwargs):
        """
        执行任务
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            task = Task.objects.get(id=pk)
        except Task.DoesNotExist:
            raise MyException("任务不存在")
        return common.response_success()

    def delete(self, request, pk, *args, **kwargs):
        """
        停止任务
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            task = Task.objects.get(id=pk)
        except Task.DoesNotExist:
            raise MyException("任务不存在")
        return common.response_success()
