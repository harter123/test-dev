import json
import threading
from interface_app import common
from interface_app.models.task import Task
from interface_app.utils.run_task_utils import RunTaskUtils
from interface_app.models.task import TASK_STATUS

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
        body = request.body
        params = json.loads(body)

        def fun(obj, arg):
            runner = RunTaskUtils(obj, arg)
            runner.run()

        t = threading.Thread(target=fun, args=(task, params))
        t.start()

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
            task.status = TASK_STATUS[2][0]
            task.save()
        except Task.DoesNotExist:
            raise MyException("任务不存在")
        return common.response_success()
