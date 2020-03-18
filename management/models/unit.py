from django.db import models


class Unit(models.Model):
    name = models.CharField(max_length=25, verbose_name="二级单位名称")

    pass
