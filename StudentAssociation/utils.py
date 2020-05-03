from django.conf import settings


from twilio.rest import Client


def send_message(phone_number, validation_code):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='+12057404952',
        body='您的验证码为',
        messaging_service_sid='MGb3ff337a5662ada54414016d113f14d7',
        to='+8618570748208'
    )

    print(message.sid, message.status)
    return True


def manager_required():
    pass


def require_manager(request, *args, **kwargs):
    pass
