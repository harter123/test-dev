from django import forms
from interface_app.fields.form.object_field import ObjectField
from interface_app.models.service import Service


class InterfaceForm(forms.Form):
    name = forms.CharField(max_length=200, required=True)
    description = forms.CharField(required=False)
    host = forms.CharField(max_length=200, required=False)
    url = forms.CharField(max_length=500, required=True)
    method = forms.CharField(required=True, max_length=20)
    header = ObjectField(required=False)
    parameter = ObjectField(required=False)
    parameter_type = forms.CharField(required=False)

    response = ObjectField(required=False)
    response_type = forms.CharField(required=False)

    service_id = forms.IntegerField(required=True)

    assertion = ObjectField(required=False)

    def clean_service_id(self):
        service_id = self.cleaned_data.get('service_id')
        try:
            Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            raise forms.ValidationError('服务不存在')
        else:
            return service_id
