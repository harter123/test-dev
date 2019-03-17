import json
from django import forms

class ObjectField(forms.Field):
    def __init__(self, *args, **kwargs):
        super(ObjectField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value is None:
            return value
        try:
            ret = json.loads(value)
        except Exception:
            return None
        else:
            return ret

    def validate(self, value):
        if not isinstance(value, dict) or not isinstance(value, list):
            raise forms.ValidationError('格式正确')