from django.conf import settings


from twilio.rest import Client


def send_message(phone_number, validation_code):
    # account_sid = "ACc79a4e5f62031921837ac70477b6e94d"
    # auth_token = "bbaafb67b7d40a0eb8a368361bc0b147"
    #
    # client = Client(account_sid, auth_token)
    #
    # message = client.messages.create(
    #     from_='+12057404952',
    #     body='body',
    #     messaging_service_sid='MGb3ff337a5662ada54414016d113f14d7',
    #     to='+8618570748208'
    # )
    #
    # print(message.sid, message.status)
    return True


def manager_required():
    pass


def require_manager(request, *args, **kwargs):
    pass
