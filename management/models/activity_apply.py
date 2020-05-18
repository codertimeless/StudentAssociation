from django.db import models


from management.models.club import Club
from accounts.models.user_profile import ClubUserProfile

TYPES = [
    ("Large-scale", "大型活动"),
    ("Regular", "常规活动"),
    ("Extension", "素拓活动")
]


class ActivityApplication(models.Model):
    apply_id = models.IntegerField(verbose_name="活动记录", primary_key=True)

    name = models.CharField(verbose_name="活动名称", max_length=30)
    main_club = models.ForeignKey(Club, verbose_name="主办社团", on_delete=models.DO_NOTHING, related_name="main")
    cooperated_club = models.ForeignKey(Club, verbose_name="协办社团", on_delete=models.DO_NOTHING,
                                        related_name="cooper", null=True, blank=True)
    activity_type = models.CharField(choices=TYPES, verbose_name="活动类型", max_length=12)
    description = models.CharField(verbose_name="活动内容", max_length=200)
    venue = models.CharField(verbose_name="活动地点", max_length=30)
    date = models.DateTimeField(verbose_name="活动预计时间")

    apply_time = models.DateTimeField(auto_created=True)
    apply_people = models.ForeignKey(ClubUserProfile, on_delete=models.DO_NOTHING)

    adjust_suggest = models.CharField(max_length=150)
    # permission
    approved_association = models.BooleanField(default=False)
    approved_teacher = models.BooleanField(default=False)
    approved_xuegong = models.BooleanField(default=False)

    def get_act_apply_info(self):
        context = {'apply': False, 'act_name': self.name, 'act_place': self.venue, 'act_type': self.activity_type,
                   'date': self.date, "coo_club": self.cooperated_club.name, 'description': self.description}
        return context
