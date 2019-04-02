import json
from django import forms

class ObjectField(forms.Field):
    def __init__(self, *args, **kwargs):
        super(ObjectField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        """
        数据从moedel读进来的时候做的处理
        :param value:
        :return:
        """
        if value is None:
            return dict()
        if isinstance(value, dict) or isinstance(value, list):
            return value
        try:
            ret = json.loads(value)
        except Exception:
            return dict()
        else:
            return ret

    def validate(self, value):
        """
        数据从前端请求进来的时候的数据校验
        :param value:
        :return:
        """
        if self.required:
            if not isinstance(value, dict) or not isinstance(value, list):
                raise forms.ValidationError('格式不正确')
        else:
            return self.to_python(value)