from django.urls import path

from .views import club_user, manage_club, activity_apply, manage_activity, activity_check, activity_info

urlpatterns = [
    path('club/', manage_club, name="manage_club"),
    path('users/', club_user, name="manage_users"),
    path('activity_apply/', activity_apply, name="apply"),
    path('activity_check/<int:activity_id>/', activity_check),
    path('activity/', manage_activity, name="activity"),
    path('activity_info/<int:activity_id>/', activity_info),
]
