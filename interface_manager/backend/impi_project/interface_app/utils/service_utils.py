from django.forms.models import model_to_dict
from interface_app.models.service import Service


class ServiceUtils:

    @classmethod
    def get_service_tree_recursion(cls, parent):
        res = []
        results = Service.objects.filter(parent=parent)
        for s in results:
            tmp = model_to_dict(s)
            tmp['children'] = ServiceUtils.get_service_tree_recursion(s.id)
            res.append(tmp)
        return res
