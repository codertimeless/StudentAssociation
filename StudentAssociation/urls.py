from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.main_view, name="main"),

    # account
    path('login/', views.login_view, name="login"),
    path('login_code/', views.login_code_view, name="login_code"),
    path('join_club/', views.join_club_view, name="join_club"),
    path('join_club/<str:club_abbr>', views.join_club_view, name="join_club"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register_view, name="register"),
    path('forget_password/', views.forget_view, name="forget"),
    path('profile/', views.profile_view, name="profile"),
    path('read_message/', views.read_message, name="read_message"),

    path('all_activity/', views.all_activities_view, name="all_activities"),

    # for message service
    path('send_msg/', views.send_msg, name="send_msg"),
    path('messages/', views.message_view, name="messages"),

    # manage club
    path('manage/', include('management.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # forum
    path("forum/", include('forum.urls')),

    path('comments/', include('comments.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
