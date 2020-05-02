from django.http import request
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone

from management.models.user_profile import ClubUserProfile


class ManageMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            try:
                profile = ClubUserProfile.objects.get(phone_number=request.user.phone_number, is_active=True)
                request.profile = profile
            except ClubUserProfile.DoesNotExist:
                request.profile = ClubUserProfile.objects.create(phone_number=request.user.phone_number, is_active=True,
                                                                 gender=request.user.gender, job="anonymous",
                                                                 joined_date=timezone.now().date())
