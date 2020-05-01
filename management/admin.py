from django.contrib import admin

import xadmin

from .models.teacher import Teacher
from .models.club import Club
from .models.unit import Unit
from .models.student import Student
from .models.activity import Activity


class TeacherAdmin(object):
    list_display = ['name', 'phone', 'affiliated_unit', 'gender']
    search_fields = ['name', 'affiliated_unit']


class StudentAdmin(object):
    list_display = ['name', 'phone', 'affiliated_unit', 'gender']
    search_fields = ['name', 'affiliated_unit']


class ActivityAdmin(object):
    list_display = ['name', 'main_club', 'date', 'activity_type', 'score']
    search_fields = ['name', 'activity_type', 'main_club']


class ClubAdmin(object):
    list_display = ['name']


class UnitAdmin(object):
    list_display = ['name']


# for xadmin
# admin.site.register(Club, ClubAdmin)
# admin.site.register(Unit, UnitAdmin)
# admin.site.register(Teacher, TeacherAdmin)
# admin.site.register(Student, StudentAdmin)
# admin.site.register(Activity, ActivityAdmin)

# for admin
admin.site.register(Club)
admin.site.register(Unit)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Activity)
