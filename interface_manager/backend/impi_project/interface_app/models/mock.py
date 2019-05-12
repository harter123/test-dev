from django.db import models
from interface_app.models.base import Base
from interface_app.fields.model.object_field import ObjectField
# Create your models here.


class Mock(models.Model, Base):
    name = models.CharField('name', blank=False, default="", max_length=200)
    description = models.TextField('description', blank=True, default='')

    method = models.CharField('method', blank=False, default="get", max_length=20)
    response = ObjectField('response', default={})

    def __str__(self):
        return self.name

