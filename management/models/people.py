from django.db import models

from .club import Club

GENDER = [
    ("female", "女"),
    ("male", "男"),
]


class People(models.Model):
    real_name = models.CharField(max_length=10, verbose_name="真实姓名")
    phone_number = models.CharField(max_length=11, verbose_name="手机", unique=True)
    club = models.ForeignKey(Club, on_delete=models.DO_NOTHING, verbose_name="社团")
    gender = models.CharField(max_length=6, choices=GENDER)

    is_active = models.BooleanField(default=True)
    joined_date = models.DateTimeField(auto_created=True)
    modify_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.real_name
