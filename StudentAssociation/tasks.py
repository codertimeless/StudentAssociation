from django.utils import timezone
from django.db.models import Q
from celery.decorators import task, periodic_task
from celery.utils.log import get_task_logger
from celery.task.schedules import crontab

from accounts.models.user_profile import ClubUserProfile
from management.models.activity_apply import ActivityApplication
from accounts.models.messages import Messages
from StudentAssociation.utils import message_service
from .utils import send_email

logger = get_task_logger(__name__)


@task(name='celery_send_email')
def celery_send_email(subject, to_email, msg):
    logger.info("Send Email")
    return send_email(subject, to_email, msg)


@task(name="send_inner_message")
def send_inner_message(content, next_url, to_user, msg_type):
    pass


@periodic_task(run_every=crontab(minute=2, hour='8-10'))
def send_msg_to_notice_check():
    aps = ActivityApplication.objects.filter(Q(approved_teacher=False) | Q(approved_association=False)
                                             | Q(approved_xuegong=False))

    for ap in aps:
        apply_time = ap.apply_time
        current_time = timezone.now()
        re = current_time - apply_time
        if re.days >= 1:
            if not ap.approved_association and not ap.send_ass:
                phone_number = ClubUserProfile.objects.filter(job="活动管理")[0].phone_number
                content = "您有一个来自 " + ap.main_club.name + " 活动申请，等待你进行审核哦，请登录社团管理系统进行查看。"
                flag, status = message_service(phone_number=phone_number, message=content)
                if flag:
                    ap.send_ass = True

            if not ap.approved_teacher and not ap.send_tea:
                phone_number = ClubUserProfile.objects.filter(job="指导老师", club=ap.main_club)[0].phone_number
                content = "您所管理的社团： " + ap.main_club.name + " ，有一个活动申请等待您的审核，请登录社团管理系统进行查看。"
                flag, status = message_service(phone_number=phone_number, message=content)
                if flag:
                    ap.send_tea = True

            if not ap.send_xue and not ap.send_xue:
                phone_number = ClubUserProfile.objects.filter(job="学工处老师")[0].phone_number
                content = "您有一个来自 " + ap.main_club.name + " 活动申请，等待你进行审核哦，请登录社团管理系统进行查看。"
                flag, status = message_service(phone_number=phone_number, message=content)
                if flag:
                    ap.send_xue = True

            ap.save()

    return True
