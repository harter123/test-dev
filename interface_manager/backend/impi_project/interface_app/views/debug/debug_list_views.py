import json
from django.views.generic import View

from interface_app import common
from interface_app.form.debug import DebugForm
from interface_app.utils.interface_utils import InterfaceUtils


# Create your views here.
# 调试功能的接口

class DebugListViews(View):
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
        form = DebugForm(params)
        result = form.is_valid()
        if result:
            url = form.cleaned_data["url"]
            method = form.cleaned_data["method"]
            header = form.cleaned_data["header"]
            parameter = form.cleaned_data["parameter"]
            parameter_type = form.cleaned_data["parameter_type"]
            ret = InterfaceUtils.send_request(url, method, header, parameter, parameter_type)
            # ret = InterfaceUtils.send_request(**form.cleaned_data)
            return common.response_success(ret)
        else:
            print(form.errors.as_json())
            return common.response_failed()
