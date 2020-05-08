from django.contrib import admin

# Register your models here.

from .models import Article


class ArticleAdmin(object):
    list_display = ['title', 'create_date', 'view', 'slug', 'category']
    search_fields = ['title', 'create_date', 'view', 'slug']


admin.site.register(Article)
