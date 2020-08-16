from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone

from accounts.models.user_profile import ClubUserProfile
from accounts.models import Messages


class ManageMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            try:
                profile = ClubUserProfile.objects.filter(phone_number=request.user.phone_number, is_active=True)
                request.profile = profile[0]
            except ClubUserProfile.DoesNotExist:
                request.profile = ClubUserProfile.objects.create(phone_number=request.user.phone_number, is_active=True,
                                                                 gender=request.user.gender, job="anonymous",
                                                                 joined_date=timezone.now().date())


class MessageMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.user.is_authenticated:
            if Messages.objects.filter(to_user=request.profile, is_read=False).exists():
                request.have_message = True
            else:
                request.have_message = False
