import json
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from interface_app import common
from interface_app.form.user import UserForm

from django.views.generic import View
from interface_app.my_exception import MyException


# Create your views here.

class UserViews(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return common.response_success({'username': user.username, 'id': user.id})
        else:
            raise MyException("用户未登录")

        # token = request.META.get("HTTP_TOKEN", None)
        # if token is None:
        #     raise MyException("用户未登录")
        # else:
        #     try:
        #         session = Session.objects.get(pk=token)
        #     except Session.DoesNotExist:
        #         raise MyException("session失效")
        #     else:
        #         user_id = session.get_decoded().get('_auth_user_id', None)
        #         if user_id is None:
        #             raise MyException("用户id失效")
        #         try:
        #             user = User.objects.get(pk=user_id)
        #         except User.DoesNotExist:
        #             raise MyException("用户不存在")
        #         else:
        #             return common.response_success({'username': user.username, 'id': user.id})

    def post(self, request, *args, **kwargs):
        body = request.body
        params = json.loads(body)
        form = UserForm(params)
        result = form.is_valid()
        if result:
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return common.response_success()
            else:
                raise MyException("注册失败")
        else:
            print(form.errors.as_json())
            raise MyException()

    def put(self, request, *args, **kwargs):
        body = request.body
        params = json.loads(body)
        form = UserForm(params)
        result = form.is_valid()
        if result:
            user = authenticate(username=form.cleaned_data["username"], password=str(form.cleaned_data["password"]))
            if user:
                login(request, user)
                return common.response_success()
            else:
                raise MyException("登录失败")
        else:
            print(form.errors.as_json())
            raise MyException()
