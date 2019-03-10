import json
import logging
from django.http import JsonResponse


def response_json(success, message, data):
    result = dict()
    result["success"] = success
    result["message"] = message
    result["data"] = data
    return JsonResponse(result, safe=False)


def response_success(data={}):
    return response_json(True, "", data)


def response_failed(message="参数错误"):
    return response_json(False, message, {})


logger = logging.getLogger(__name__)
