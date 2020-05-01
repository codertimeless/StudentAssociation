from django.db import models

from .people import People
from .student_class import StudentClass


class NormalUserProfile(People):
    student_number = models.CharField(max_length=10, verbose_name="学号", unique=True)
    # 班级
    student_class = models.ForeignKey(StudentClass, on_delete=models.DO_NOTHING, verbose_name="")


class ClubUserProfile(People):
    pass


class TeacherUserProfile(People):

