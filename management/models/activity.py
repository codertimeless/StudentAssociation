from django.db import models

from ..models.club import Club
from .activity_apply import ActivityApplication


# the activity after apply
class Activity(models.Model):
    active_id = models.IntegerField(primary_key=True)
    activity_application = models.ForeignKey(ActivityApplication, on_delete=models.DO_NOTHING)

    # date time about a activity
    start_date = models.DateTimeField(verbose_name="活动开始时间", null=True)
    end_date = models.DateTimeField(verbose_name="活动结束时间", null=True)
    score = models.IntegerField(verbose_name="活动分数", null=True, blank=True)

    people_count = models.IntegerField(verbose_name="活动参与人数", null=True)

    # to identify if a activity over or not
    is_over = models.BooleanField(default=False)

    def __str__(self):
        return self.activity_application.name
