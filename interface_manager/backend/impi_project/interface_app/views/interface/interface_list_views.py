import json
from django.forms.models import model_to_dict
from django.views.generic import View

from interface_app import common
from interface_app.form.interface import InterfaceForm
from interface_app.models.interface import Interface
from interface_app.my_exception import MyException


# Create your views here.
# interface的列表获取和创建的接口

class InterfaceListViews(View):
    def get(self, request, *args, **kwargs):
        """
        获取全部接口列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        interfaces = Interface.objects.all() # model对象不能直接返回前端，需要转字典
        ret = []
        for i in interfaces:
            ret.append(model_to_dict(i))
        # ret = [model_to_dict(i) for i in interfaces]
        return common.response_success(ret)

    def post(self, request, *args, **kwargs):
        """
        创建接口
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        body = request.body
        params = json.loads(body)
        form = InterfaceForm(params)
        result = form.is_valid()
        if result:
            interface = Interface.objects.create(**form.cleaned_data)
            if interface:
                return common.response_success()
            else:
                raise MyException("创建失败")
        else:
            print(form.errors.as_json())
            return common.response_failed()
