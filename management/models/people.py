from django.db import models

from ..models.unit import Unit

GENDER = [
    ("female", "女"),
    ("male", "男"),
]


class People(models.Model):
    name = models.CharField(max_length=20, verbose_name="姓名")
    phone = models.CharField(max_length=11, verbose_name="联系电话")
    gender = models.CharField(max_length=6, choices=GENDER)
    affiliated_unit = models.ForeignKey(Unit, on_delete=models.DO_NOTHING)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
