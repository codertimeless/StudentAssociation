from django.db import models

from management.models.club import Club
from accounts.models.user_profile import ClubUserProfile

TYPES = [
    ("大型活动", "大型活动"),
    ("常规活动", "常规活动"),
    ("素拓活动", "素拓活动")
]

AP_STATUS = [
    ("审核中", "审核中"),
    ("学社联要求修改", "学社联要求修改"),
    ("学社联同意", "学社联同意"),
    ("学社联拒绝", "学社联拒绝"),
    ("等待指导老师审核", "等待指导老师审核"),
    ("指导老师要求修改", "指导老师要求修改"),
    ("指导老师已拒绝", "指导老师已拒绝"),
    ("待举办", "待举办"),
    ("已完成", "已完成"),
]


class ActivityApplication(models.Model):
    name = models.CharField(verbose_name="活动名称", max_length=30)
    main_club = models.ForeignKey(Club, verbose_name="主办社团", on_delete=models.DO_NOTHING, related_name="main")
    cooperated_club = models.ForeignKey(Club, verbose_name="协办社团", on_delete=models.DO_NOTHING,
                                        related_name="cooper", null=True, blank=True)
    activity_type = models.CharField(choices=TYPES, verbose_name="活动类型", max_length=12)
    description = models.CharField(verbose_name="活动内容", max_length=200)
    venue = models.CharField(verbose_name="活动地点", max_length=30)
    date = models.DateTimeField(verbose_name="活动预计时间")

    apply_time = models.DateTimeField(auto_now_add=True)
    apply_people = models.ForeignKey(ClubUserProfile, on_delete=models.DO_NOTHING)

    adjust_suggest_ass = models.CharField(max_length=150, null=True)
    adjust_suggest_tea = models.CharField(max_length=150, null=True)

    # permission
    approved_association = models.BooleanField(default=False)
    send_ass = models.BooleanField(default=False)
    approved_teacher = models.BooleanField(default=False)
    send_tea = models.BooleanField(default=False)
    approved_xuegong = models.BooleanField(default=False)
    send_xue = models.BooleanField(default=False)

    denied = models.BooleanField(default=False)
    request_change = models.BooleanField(default=False)

    ap_status = models.CharField(max_length=20, choices=AP_STATUS)
    is_check_over = models.BooleanField(default=False)
    is_over = models.BooleanField(default=False)

    def get_act_apply_info(self):
        context = {'apply': False, 'act_name': self.name, 'act_place': self.venue, 'act_type': self.activity_type,
                   'date': self.date, 'description': self.description, 'apply_time': self.apply_time,
                   "status": self.is_check_over, "sug_ass": self.adjust_suggest_ass, "sug_tea": self.adjust_suggest_tea,
                   "ap_status": self.ap_status}

        if self.cooperated_club:
            context['coo_club'] = self.cooperated_club.name

        return context

    def __str__(self):
        return self.main_club.name + ": " + self.name
