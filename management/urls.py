from django.urls import path

from .views import club_user, manage_club

urlpatterns = [
    path('club/', manage_club),
    path('users/', club_user),

]
