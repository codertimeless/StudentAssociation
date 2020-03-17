from django.db import models

from ..models.club import Club

types = [
    ("大型活动", "Large-scale"),
    ("常规活动", "Regular"),
    ("素拓活动", "Extension")
]


class Activity(models.Model):
    name = models.CharField(verbose_name="活动名称", max_length=30)

    mainClub = models.ForeignKey(Club, verbose_name="主办社团", on_delete=models.DO_NOTHING, related_name="main")
    cooperatedClub = models.ForeignKey(Club, verbose_name="协办社团", on_delete=models.DO_NOTHING, related_name="cooper")
    activityType = models.CharField(choices=types, verbose_name="活动类型", max_length=12)

    description = models.CharField(verbose_name="活动内容", max_length=200)
    date = models.DateTimeField(verbose_name="活动时间")
    peopleCount = models.IntegerField(verbose_name="活动参与人数")
    venue = models.CharField(verbose_name="活动地点", max_length=30)
    score = models.IntegerField(verbose_name="活动分数")

    def __str__(self):
        return "%s - %s" % (self.mainClub, self.name)
