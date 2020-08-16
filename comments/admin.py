from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'created_time']
    fields = ['name', 'url', 'text', 'post']


admin.site.register(Comment, CommentAdmin)
