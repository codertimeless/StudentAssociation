from django.urls.conf import path

from .views import article_view, forum_view, write_article

urlpatterns = [
    path('article/<int:article_id>', article_view),
    path('index/', forum_view, name="forum_index"),
    path('write/', write_article, name="write_article"),

]
