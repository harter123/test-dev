from django.forms.models import model_to_dict
from interface_app.models.result import TaskResult, InterfaceResult


class TaskUtils:

    @classmethod
    def get_result_summary(cls, result_id):
        ret = {
            "success": 0,
            "failed": 0,
            "total": 0
        }
        if not result_id:
            return ret

        v = InterfaceResult.objects.filter(task_result_id=result_id)
        for i in v:
            if i.success:
                ret["success"] += ret["success"]
            else:
                ret["failed"] += ret["failed"]
        ret["total"] = ret["success"] + ret["failed"]
        return ret

    @classmethod
    def get_last_result_summary(cls, task_id):
        if not task_id:
            return cls.get_result_summary(None)
        result = cls.get_last_result(task_id)
        if result is None:
            return cls.get_result_summary(None)
        ret = cls.get_result_summary(result.id)
        return ret

    @classmethod
    def get_last_result(cls, task_id):
        if not task_id:
            return None
        results = TaskResult.objects.filter(task_id=task_id).order_by('-version')
        if 0 == len(results):
            return None
        return results[0]

    @classmethod
    def get_last_interface_result(cls, result_id, interface_id):
        if not result_id or not interface_id:
            return "无"
        v = InterfaceResult.objects.filter(task_result_id=result_id, interface_id=interface_id)
        if 0 == len(v):
            return '无'

        if v[0].success:
            return "成功"
        else:
            return "失败"