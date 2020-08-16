from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from comments.models import Comment
from StudentAssociation.utils import send_inner_message
from django.contrib.auth.decorators import login_required

from accounts.models.user_profile import ClubUserProfile
from forum.models import Article


@require_POST
@login_required(login_url='/login')
def comment(request, post_pk):
    article = get_object_or_404(Article, pk=post_pk)
    content = request.POST.get("content", "")
    context = {
        'article': article,
    }

    if content:
        user_comment = Comment.objects.create(text=content, author=request.user, post=article)
        user_comment.save()
        article.comment_num += 1
        article.save()
        if request.user != article.author:
            content = "您在论坛发表的文章" + ' "' + article.title + '"，' + request.user.username + "评论了，快去看看吧"
            to_user = ClubUserProfile.objects.get(phone_number=article.author.phone_number)
            next_url = "/forum/article/" + str(article.pk)
            message_type = "论坛消息"
            send_inner_message(content, to_user, next_url, message_type)

        return redirect('forum_article', article_id=article.pk)

    return redirect('forum_article', article_id=article.pk)


@require_POST
def del_comment(request, com_pk):
    try:
        the_comment = Comment.objects.get(pk=com_pk)
        article_id = the_comment.post.pk
        the_comment.delete()
        post = the_comment.post
        post.comment_num -= 1
        post.save()
    except Comment.DoesNotExist:
        pass

    return redirect('forum_article', article_id=article_id)


