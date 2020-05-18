from django.contrib import admin


from .models import Article


class ArticleAdmin(object):
    list_display = ['title', "author"]


admin.site.register(Article)
