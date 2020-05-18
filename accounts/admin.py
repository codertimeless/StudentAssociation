from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models.studentclub_user import StudentClubUser
from .models.user_profile import ClubUserProfile
from .models import Messages


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('phone_number', 'username')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('is_superuser',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2')}
         ),
    )
    search_fields = ('phone_number',)
    ordering = ('phone_number',)
    filter_horizontal = ()


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'real_name', 'phone_number', 'club', 'student_class', 'job')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'from_user', 'to_user')


admin.site.register(StudentClubUser, UserAdmin)
admin.site.register(ClubUserProfile, ProfileAdmin)
admin.site.register(Messages, MessageAdmin)
