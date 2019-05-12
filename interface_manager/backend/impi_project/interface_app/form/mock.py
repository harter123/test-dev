from django import forms
from interface_app.fields.form.object_field import ObjectField


class MockForm(forms.Form):
    name = forms.CharField(max_length=200, min_length=1, required=True,)
    description = forms.CharField(min_length=1, required=True,)
    method = forms.CharField(required=True, max_length=200,)
    response = ObjectField(required=False)
