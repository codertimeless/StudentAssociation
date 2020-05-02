from django.urls import path, include
from django.contrib import admin


import xadmin

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls, name="xadmin-login"),
    path('', views.main_view, name="index"),

    # account
    path('login/', views.login_view, name="login"),
    path('join_club/', views.join_club_view, name="join_club"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register_view, name="register"),
    path('forget/', views.forget_view, name="forget"),
    path('send_msg/', views.send_msg, name="sms"),
    # manage club
    path('manage/', include('management.urls'))
]
