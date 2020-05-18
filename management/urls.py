from django.urls import path

from .views import club_user, manage_club, activity_apply, manage_activity

urlpatterns = [
    path('club/', manage_club, name="manage_club"),
    path('users/', club_user, name="manage_users"),
    path('activity_apply/<int: activity_id>/', activity_apply, name="apply"),
    path('activity_apply/', activity_apply, name="apply"),
    path('activity/', manage_activity, name="activity"),

]
