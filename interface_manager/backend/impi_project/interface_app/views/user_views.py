import json
from django.contrib.sessions.models import Session
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
            user = User.objects.create_user(username=str(params["name"]), password=str(params["pwd"]))
            if user:
                login(request, user)

                session = request.session.session_key
                return common.response_success({'session': session})
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
                login(request, user)
                session = request.session.session_key
                return common.response_success({'session': session})
            else:
                return common.response_failed("登录失败")
        else:
            return common.response_failed("参数不正确")
    else:
        return HttpResponse(status=404)


def get_user(request):
    if "GET" == request.method:

        # user = request.user
        # if user.is_authenticated:
        #     return common.response_success({'username': user.username, 'id': user.id})
        # else:
        #     return common.response_failed("用户未登录")
        token = request.META.get("HTTP_TOKEN", None)
        if token is None:
            return common.response_failed("用户未登录")
        else:
            try:
                session = Session.objects.get(pk=token)
            except Session.DoesNotExist:
                return common.response_failed("session失效")
            except Exception as e:
                print(e)
                return common.response_failed("未知错误")
            else:
                user_id = session.get_decoded().get('_auth_user_id', None)
                if user_id is None:
                    return common.response_failed("用户id失效")
                try:
                    user = User.objects.get(pk=user_id)
                except User.DoesNotExist:
                    return common.response_failed("用户不存在")
                else:
                    return common.response_success({'username': user.username, 'id': user.id})
    else:
        return HttpResponse(status=404)
