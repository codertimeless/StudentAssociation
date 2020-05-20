from django.db import models
from django.utils import timezone

from management.models.student_class import StudentClass
from management.models.unit import Unit
from management.models.club import Club

GENDER = [
    ("female", "女"),
    ("male", "男"),
    ("unknown", "未知")
]

JOBS = [
    ("指导老师", "指导老师"),
    ("会长", "会长"),
    ("副会长", "副会长"),
    ("成员", "成员"),
    ("匿名", "匿名")
]


class ClubUserProfile(models.Model):
    real_name = models.CharField(max_length=10, verbose_name="真实姓名")
    phone_number = models.CharField(max_length=11, verbose_name="手机")
    club = models.ForeignKey(Club, on_delete=models.DO_NOTHING, verbose_name="社团", null=True)
    gender = models.CharField(max_length=7, choices=GENDER)

    # by phone_number
    # user = models.ForeignKey(StudentClubUser, null=True, blank=True, on_delete=models.DO_NOTHING)

    joined_date = models.DateTimeField(default=timezone.now())
    modify_date = models.DateTimeField(auto_now=True)

    # permissions
    is_active = models.BooleanField(default=True)
    job = models.CharField(choices=JOBS, max_length=12, default="匿名")
    is_manager = models.BooleanField(default=False)

    # for student
    student_class = models.ForeignKey(StudentClass, on_delete=models.DO_NOTHING, verbose_name="班级", null=True)
    student_number = models.CharField(max_length=10, verbose_name="学号", null=True, blank=True)

    # for teacher
    unit = models.ForeignKey(Unit, on_delete=models.DO_NOTHING, verbose_name="单位", null=True, blank=True)

    def __str__(self):
        return self.real_name

    def flush_all_expiration_user_profile(self, date):
        if self.joined_date < date and self.job != "teacher":
            self.is_active = False
