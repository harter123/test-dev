import json
from django.forms.models import model_to_dict
from interface_app import common
from interface_app.form.service import ServiceForm
from interface_app.models.service import Service

from django.views.generic import View
from interface_app.my_exception import MyException


# Create your views here.

class ServiceDetailViews(View):
    def get(self, request, pk, *args, **kwargs):
        """
        获取单个服务
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            service = Service.objects.get(id=pk)
        except Service.DoesNotExist:
            return common.response_failed()
        else:
            return common.response_success(model_to_dict(service))

    def put(self, request, pk, *args, **kwargs):
        """
        更新单个服务
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        body = request.body
        params = json.loads(body)
        form = ServiceForm(params)  # 参数校验
        result = form.is_valid()
        if result:
            Service.objects.filter(id=pk).update(**form.cleaned_data)
            # Service.objects.filter(id=pk).update(name=form.cleaned_data['name'],
            #                                      description=form.cleaned_data['name'],
            #                                      parent=form.cleaned_data['parent'])
        else:
            print(form.errors.as_json())
            raise MyException()
        return common.response_success()

    def delete(self, request, pk, *args, **kwargs):
        """
        删除单个服务
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        Service.objects.filter(id=pk).delete()
        return common.response_success()
