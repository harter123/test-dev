from django.forms.models import model_to_dict
from interface_app import common
from interface_app.models.interface import Interface

from django.views.generic import View


# Create your views here.
# 获取某个服务下的interface列表

class ServiceInterfaceDetailViews(View):
    def get(self, request, pk, *args, **kwargs):
        """
        获取单个服务
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        interfaces = Interface.objects.filter(service_id=pk)
        ret = []
        for i in interfaces:
            ret.append(model_to_dict(i))
        return common.response_success(model_to_dict(ret))

