from django.http import request
from django.utils.deprecation import MiddlewareMixin


from management.models.user_profile import NormalUserProfile, Clubu


class ManageMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            phone_number = request.user.phone_number
            if request.user.is_club_manage:



