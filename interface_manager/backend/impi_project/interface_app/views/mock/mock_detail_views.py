import json
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.generic import View

from interface_app import common
from interface_app.form.mock import MockForm
from interface_app.models.mock import Mock
from interface_app.my_exception import MyException


# Create your views here.
# mock获取，修改，删除接口

class MockDetailViews(View):
    def get(self, request, pk, *args, **kwargs):
        """
        获取单个mock
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            mock = Mock.objects.get(id=pk)
        except Mock.DoesNotExist:
            return common.response_failed()
        else:
            return common.response_success(model_to_dict(mock))

    def put(self, request, pk, *args, **kwargs):
        """
        更新单个mock
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        body = request.body
        params = json.loads(body)
        form = MockForm(params)  # 参数校验
        result = form.is_valid()
        if result:
            Mock.objects.filter(id=pk).update(**form.cleaned_data)
        else:
            print(form.errors.as_json())
            raise MyException()
        return common.response_success()

    def delete(self, request, pk, *args, **kwargs):
        """
        删除单个mock
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        Mock.objects.filter(id=pk).delete()
        return common.response_success()


def run_mock(request, pk):
    if not pk:
        raise MyException()
    mock = Mock.objects.get(id=pk)
    if request.method == mock.method:
        return JsonResponse(mock.response, safe=False)
    else:
        raise MyException("mock不存在")
