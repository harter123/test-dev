import json
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from interface_app import common


# Create your views here.

def register_user(request):
    if "POST" == request.method:
        body = request.body
        params = json.loads(body)
        if "name" in params and "" != str(params["name"]) and "pwd" in params and "" != str(params["pwd"]):
            # user = User(username=str(params["name"]), password=str(params["pwd"]))
            # user.save()
            result = User.objects.create_user(username=str(params["name"]), password=str(params["pwd"]))
            if result:
                return common.response_success()
            else:
                return common.response_failed("注册失败")
        else:
            return common.response_failed("参数不正确")
    else:
        return HttpResponse(status=404)


def login_user(request):
    if "POST" == request.method:
        body = request.body
        params = json.loads(body)
        if "name" in params and "" != str(params["name"]) and "pwd" in params and "" != str(params["pwd"]):
            user = authenticate(username=params["name"], password=str(params["pwd"]))
            if user:
                return common.response_success()
            else:
                return common.response_failed("登录失败")
        else:
            return common.response_failed("参数不正确")
    else:
        return HttpResponse(status=404)
