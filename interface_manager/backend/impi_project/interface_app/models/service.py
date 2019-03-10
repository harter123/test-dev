from django.db import models

# Create your models here.
IS_ROOT = 0


class Service(models.Model):
    name = models.CharField('name', blank=False, default="", max_length=200)
    description = models.TextField('description', blank=True, default='')
    parent = models.IntegerField('父节点', blank=False, default=IS_ROOT)

    def __str__(self):
        return self.name
