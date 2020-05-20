from django.contrib import admin

from .models.club import Club
from .models.unit import Unit
from .models.activity import Activity
from .models.activity_apply import ActivityApplication
from .models.student_class import StudentClass


class ActivityAdmin(object):
    list_display = ['name', 'main_club', 'date', 'activity_type', 'score']
    search_fields = ['name', 'activity_type', 'main_club']


class ClubAdmin(object):
    list_display = ['name']


class UnitAdmin(object):
    list_display = ['name']


class ActivityApplicationAdmin(object):
    list_display = ['name']


class StudentClassAdmin(object):
    list_display = ["unit", "classname"]


# for admin
admin.site.register(Club)
admin.site.register(ActivityApplication)
admin.site.register(Unit)
admin.site.register(Activity)
admin.site.register(StudentClass)
