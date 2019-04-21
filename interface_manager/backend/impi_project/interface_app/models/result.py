from django.db import models
from interface_app.models.base import Base
from interface_app.models.interface import Interface
from interface_app.fields.model.object_field import ObjectField
from interface_app.models.task import Task

# Create your models here.

class TaskResult(models.Model, Base):
    version = models.IntegerField('version', default=1)
    created = models.DateTimeField("创建时间", auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.version


class InterfaceResult(models.Model, Base):
    """
    接口的请求历史结果版本
    """
    interface = models.ForeignKey(Interface, on_delete=models.SET_NULL, null=True)
    task_result = models.ForeignKey(TaskResult, on_delete=models.SET_NULL, null=True)

    name = models.CharField('name', blank=False, max_length=200)
    description = models.TextField('description', default='')

    host = models.CharField('host', default="", max_length=200)
    url = models.CharField('url', blank=False, max_length=500)
    method = models.CharField('method', blank=False, max_length=20)

    header = ObjectField('header', default={})
    parameter = ObjectField('parameter', default={})
    parameter_type = models.CharField('parameter_type, json or form', default="json", max_length=20)

    response = ObjectField('response', default="")
    response_type = models.CharField('response_type, json or html', default="json", max_length=20)

    assertion = ObjectField('assertion', default=[])

    created = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.name
