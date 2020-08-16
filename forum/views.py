from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http.response import HttpResponse
from django.template import loader
from .models import Article
from django.shortcuts import render

# Create your views here.


def article_view(request, article_id):
    context = {}
    try:
        article = Article.objects.get(pk=article_id)

        if "art_%s_read" % article_id not in request.COOKIES:
            article.read_num += 1
            article.save()
    except Article.DoesNotExist:
        return render(request, "blog/article_v1.html", context=context)

    context['article'] = article
    content = loader.render_to_string("blog/article_v1.html", context=context, request=request)
    response = HttpResponse(content)
    response.set_cookie("art_%s_read" % article_id, "True")
    return response


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
        context = {'error': True, 'error_message': "文章成功提交审核！", 'message_type': "提示"}

        return render(request, "blog/write_v1.html", context=context)


def search_view(request):
    q = request.GET.get("q")
    context = {'search': True}

    if q:
        articles = Article.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)
                                          | Q(author__username__icontains=q) | Q(tags__icontains=q)
                                          | Q(description__icontains=q))

        articles = articles.filter(is_active=True, is_validate=True)
        context['articles'] = articles

    return render(request, "blog/index_v1.html", context=context)
