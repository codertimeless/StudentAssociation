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
    return render(request, "blog/index_v1.html")


@login_required(login_url='/login/')
def write_article(request):

    return render(request, "blog/write_v1.html")

