from django.db import models
from django.utils import timezone

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from accounts.models.studentclub_user import StudentClubUser

TAGS = [
    ("活动记录", "活动记录"),
    ("教程分享", "教程分享"),
    ("日常分享", "日常分享"),
]


class Article(models.Model):
    title = models.CharField(max_length=20, verbose_name="标题")
    author = models.ForeignKey(StudentClubUser, verbose_name="作者", on_delete=models.DO_NOTHING)
    tags = models.CharField(max_length=4, verbose_name="标签", choices=TAGS)
    content = RichTextUploadingField(verbose_name="文章内容")
    description = RichTextField(verbose_name="文章简介")

    # status
    read_num = models.IntegerField(verbose_name="阅读量", default=0)
    zan_num = models.IntegerField(verbose_name="点赞量", default=0)
    comment_num = models.IntegerField(verbose_name="评论量", default=0)

    created_time = models.DateTimeField(default=timezone.now())
    modify_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    modify_suggest = RichTextField(verbose_name="修改意见", null=True)
    is_validate = models.BooleanField(default=False)
