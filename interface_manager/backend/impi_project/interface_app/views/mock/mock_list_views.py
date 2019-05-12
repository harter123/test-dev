import json
from interface_app import common
from interface_app.form.mock import MockForm
from interface_app.models.mock import Mock
from django.forms.models import model_to_dict

from django.views.generic import View
from interface_app.my_exception import MyException


# Create your views here.
# mock的列表获取和创建的接口

class MockListViews(View):
    def get(self, request, *args, **kwargs):
        """
        获取mock列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        mocks = Mock.objects.all()  # model对象不能直接返回前端，需要转字典
        ret = []
        for i in mocks:
            ret.append(model_to_dict(i))
        return common.response_success(ret)

    def post(self, request, *args, **kwargs):
        """
        创建mock
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        body = request.body
        params = json.loads(body)
        form = MockForm(params)
        result = form.is_valid()
        if result:
            mock = Mock.objects.create(**form.cleaned_data)
            if mock:
                return common.response_success()
            else:
                raise MyException("创建失败")
        else:
            print(form.errors.as_json())
            return common.response_failed()
