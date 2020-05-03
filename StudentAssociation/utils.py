from django.conf import settings


from twilio.rest import Client


def message_service(phone_number, random_code):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN

    client = Client(account_sid, auth_token)
    phone_number = "+86" + phone_number
    message = client.messages.create(
        from_='+12057404952',
        body=random_code,
        messaging_service_sid='MGb3ff337a5662ada54414016d113f14d7',
        to=phone_number,
    )
    return message.status


def manager_required():
    pass


def require_manager(request, *args, **kwargs):
    pass
