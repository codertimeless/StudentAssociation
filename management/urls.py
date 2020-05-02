from django.urls import path, include

from .views import club_user, manage_club

urlpatterns = [
    path('', manage_club),
    path('users/', club_user),

]
