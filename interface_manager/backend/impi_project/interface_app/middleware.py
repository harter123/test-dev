# -*- coding: UTF-8 -*-
import traceback
from django.utils.deprecation import MiddlewareMixin
from django.db import DatabaseError
from interface_app.my_exception import MyException
from interface_app.common import response_failed


class MyExceptionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print("请求进来")
        # if "/backend/user/" == request.path:
        #     return
        #
        # if request.user.is_authenticated:
        #     return
        # else:
        #     raise MyException("用户未登录")

    def process_response(self, request, response):
        print("响应返回")
        return response

    def process_exception(self, request, exception):
        print(traceback.print_exc())
        if isinstance(exception, MyException):
            print('这是我的错误')
            return response_failed(exception.message)

        elif isinstance(exception, DatabaseError):
            print('数据库错误')
            return response_failed('数据库错误')
        else:
            print('未知错误')
            return response_failed('未知错误')
