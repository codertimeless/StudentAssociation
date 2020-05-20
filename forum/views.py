from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Article
# Create your views here.


def article_view(request, article_id):
    context = {}
    article = Article.objects.get(pk=article_id)
    context['article'] = article
    return render(request, "blog/article_v1.html", context=context)


def forum_view(request):
    context = {}
    articles = Article.objects.filter(is_active=True, is_validate=True)
    art_type = request.GET.get("type", "")
    if art_type == "教程分享":
        articles = articles.filter(tags="教程分享")
    elif art_type == "活动记录":
        articles = articles.filter(tags="活动记录")
    elif art_type == "社联文章":
        articles = articles.filter(tags="社联文章")

    order = request.GET.get("order", "")
    if order == "comment":
        articles = articles.order_by('-comment_num')
    elif order == "time":
        articles = articles.order_by('-created_time')

    context['articles'] = articles

    return render(request, "blog/index_v1.html", context=context)


@login_required(login_url='/login/')
def write_article(request):
    if request.method == "GET":
        return render(request, "blog/write_v1.html")

    elif request.method == "POST":
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        tag = request.POST.get("tag", "")
        content = request.POST.get("content", "")

        author = request.user
        if title and description and tag and content and author:
            article = Article.objects.get_or_create(title=title, author=author,
                                                    tags=tag, content=content, description=description)

        return render(request, "blog/write_v1.html")
