from django import forms
from interface_app.fields.form.object_field import ObjectField


class DebugForm(forms.Form):
    """
    调试功能的参数检验
    """
    url = forms.CharField(max_length=500, required=True)
    method = forms.CharField(required=True, max_length=20)
    header = ObjectField(required=False)
    parameter = ObjectField(required=False)
    parameter_type = forms.CharField(required=False)
