from django.db import models

from ..models.club import Club

TYPES = [
    ("Large-scale", "大型活动"),
    ("Regular", "常规活动"),
    ("Extension", "素拓活动")
]


class Activity(models.Model):
    name = models.CharField(verbose_name="活动名称", max_length=30)

    main_club = models.ForeignKey(Club, verbose_name="主办社团", on_delete=models.DO_NOTHING, related_name="main")
    cooperated_club = models.ForeignKey(Club, verbose_name="协办社团", on_delete=models.DO_NOTHING,
                                        related_name="cooper", null=True, blank=True)
    activity_type = models.CharField(choices=TYPES, verbose_name="活动类型", max_length=12)

    description = models.CharField(verbose_name="活动内容", max_length=200)
    date = models.DateTimeField(verbose_name="活动时间")
    people_count = models.IntegerField(verbose_name="活动参与人数")
    venue = models.CharField(verbose_name="活动地点", max_length=30)
    score = models.IntegerField(verbose_name="活动分数")

    def __str__(self):
        return self.name
