from django.db import models
from django.utils import timezone

from forum.models.article import Article
from accounts.models.studentclub_user import StudentClubUser


class Comment(models.Model):
    name = models.CharField('名字', max_length=50, null=True)
    author = models.ForeignKey(StudentClubUser, on_delete=models.DO_NOTHING, null=True)

    url = models.URLField('网址', blank=True, null=True)
    text = models.TextField('内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    post = models.ForeignKey(Article, verbose_name='文章', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}: {}'.format(self.name, self.text[:20])
