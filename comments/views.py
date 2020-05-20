from forum.models import Article
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from comments.models import Comment


@require_POST
def comment(request, post_pk):
    article = get_object_or_404(Article, pk=post_pk)
    content = request.POST.get("content", "")
    context = {
        'article': article,
    }

    if content:
        user_comment = Comment.objects.create(text=content, name=request.user.username, post=article)
        user_comment.save()
        return render(request, "blog/article_v1.html", context)

    return render(request, 'blog/article_v1.html', context=context)
