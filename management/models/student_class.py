from django.db import models
from django.utils import timezone


from .unit import Unit


class StudentClass(models.Model):
    unit = models.ForeignKey(Unit, verbose_name="学院", on_delete=models.DO_NOTHING)
    # year = models.IntegerField(default=timezone.now().year)
    classname = models.CharField(max_length=20, verbose_name="专业班级")

    def __str__(self):
        return self.classname
    # def get_different_discipline(self):
    #     disciplines = self.discipline
    #     if disciplines:
    #         return disciplines.split("，")
    #
    # def get_full_class_name(self):
    #     return self.unit + self.classname
