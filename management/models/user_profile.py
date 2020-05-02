from django.db import models


from .student_class import StudentClass
from .unit import Unit
from .club import Club
from accounts.models.studentclub_user import StudentClubUser

GENDER = [
    ("female", "女"),
    ("male", "男"),
]

JOBS = [
    ("teacher", "指导老师"),
    ("manager", "会长"),
    ("vicemanager", "副会长"),
    ("member", "成员"),
    ("anonymous", "匿名")
]


class ClubUserProfile(models.Model):
    real_name = models.CharField(max_length=10, verbose_name="真实姓名")
    phone_number = models.CharField(max_length=11, verbose_name="手机")
    club = models.ForeignKey(Club, on_delete=models.DO_NOTHING, verbose_name="社团", null=True)
    gender = models.CharField(max_length=6, choices=GENDER)

    # by phone_number
    # user = models.ForeignKey(StudentClubUser, null=True, blank=True, on_delete=models.DO_NOTHING)

    joined_date = models.DateTimeField(auto_created=True)
    modify_date = models.DateTimeField(auto_now=True)

    # permissions
    is_active = models.BooleanField(default=True)
    job = models.CharField(choices=JOBS, max_length=12)

    # for student
    student_class = models.ForeignKey(StudentClass, on_delete=models.DO_NOTHING, verbose_name="职务", null=True, blank=True)
    student_number = models.CharField(max_length=10, verbose_name="学号", null=True, blank=True)

    # for teacher
    unit = models.ForeignKey(Unit, on_delete=models.DO_NOTHING, verbose_name="单位", null=True, blank=True)

    def __str__(self):
        return self.real_name

    def flush_all_expiration_user_profile(self, date):
        if self.joined_date < date and self.job != "teacher":
            self.is_active = False
