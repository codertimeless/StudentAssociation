from django.urls import path

from . import views

app_name = 'comments'

urlpatterns = [
    path('comment/<int:post_pk>', views.comment, name='comment'),
    path('delete/<int:com_pk>', views.del_comment, name="del_com"),
]
