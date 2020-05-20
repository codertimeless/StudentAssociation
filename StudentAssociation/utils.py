from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from accounts.models import Messages


def message_service(phone_number, random_code, message=None):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN

    client = Client(account_sid, auth_token)
    phone_number = "+86" + phone_number
    if random_code:
        body = "您的验证码为：" + str(random_code) + "，请在 5分钟以内使用该验证码进行相关操作。"
    if message:
        body = message
    try:
        message = client.messages.create(
            from_='+12057404952',
            body=body,
            messaging_service_sid='MGb3ff337a5662ada54414016d113f14d7',
            to=phone_number,
        )
    except TwilioRestException:
        return False, 404

    return True, message.status


def get_info_from_cache(phone_number, usage):
    try:
        info = cache.get(phone_number + usage)
        return info
    except:
        return False


def manager_required():
    pass


def require_manager(request, *args, **kwargs):
    pass


# @app.task
def send_email(subject, to_email, msg):
    try:
        send_mail(
            subject=subject,
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email]
        )
    except Exception:
        return "send email failed."

    return "send email success."


def send_inner_message(to_user, content):
    pass
