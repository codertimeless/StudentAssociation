from django.db import models

from .studentclub_user import StudentClubUser
from .user_profile import ClubUserProfile

MESSAGE_TYPES = [
    ("社联消息", "社联消息"),
    ("活动消息", "活动消息"),
    ("论坛消息", "论坛消息"),
]


class Messages(models.Model):
    content = models.CharField(max_length=100, verbose_name="消息内容")
    next_url = models.CharField(max_length=120, verbose_name="详情页面")
    created_time = models.DateTimeField(auto_now=True)
    from_user = models.ForeignKey(StudentClubUser,
                                  verbose_name="发送人",
                                  related_name="message_from",
                                  on_delete=models.DO_NOTHING, null=True, blank=True
                                  )
    to_user = models.ForeignKey(ClubUserProfile,
                                verbose_name="接受人",
                                related_name="message_to",
                                on_delete=models.DO_NOTHING)

    is_read = models.BooleanField(default=False)
    type = models.CharField(choices=MESSAGE_TYPES, max_length=4, verbose_name="消息类型")

    class Meta:
        ordering = ["-created_time"]
