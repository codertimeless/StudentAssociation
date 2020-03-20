from .models.teacher import Teacher
from .models.club import Club
from .models.unit import Unit
from .models.student import Student
from .models.activity import Activity

import xadmin


class TeacherAdmin(object):
    list_display = ['name', 'phone', 'affiliated_unit', 'gender']
    search_fields = ['name', 'affiliated_unit']


class StudentAdmin(object):
    list_display = ['name', 'phone', 'affiliated_unit', 'gender']
    search_fields = ['name', 'affiliated_unit']


class ActivityAdmin(object):
    list_display = ['name', 'main_club', 'date', 'activity_type', 'score']
    search_fields = ['name', 'activity_type', 'main_club']


xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(Student, StudentAdmin)
xadmin.site.register(Activity, ActivityAdmin)

