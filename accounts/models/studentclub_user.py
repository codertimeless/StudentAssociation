from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from management.models.user_profile import ClubUserProfile


class StudentClubUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Creates and saves a User with the given phone_number and password.
        """
        if not phone_number:
            raise ValueError('用户必须填写手机号码')

        user = self.model(
            phone_number=self.normalize_number(phone_number),
        )

        user.set_password(password)
        user.is_active = True
        try:
            user_profile = ClubUserProfile.objects.get(phone_number=phone_number, is_active=True)
            user.user_profile = user_profile
        except :
            user.is_anonymous = True

        user.save(using=self._db)
        return user

    def create_staffuser(self, phone_number, password):
        """
        Creates and saves a staff user with the given phone_number and password.
        """
        user = self.create_user(
            phone_number,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        """
        Creates and saves a superuser with the given phone_number and password.
        """
        user = self.create_user(
            phone_number,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
    def normalize_number(self, phone_number):
        if isinstance(phone_number, str):
            return phone_number
        

class StudentClubUser(AbstractUser):
    phone_number = models.CharField(verbose_name="手机号码", max_length=15, unique=True)
    username = models.CharField(
        null=True, blank=True, max_length=15, default_nickname="用户"
    )

    # admin permissions
    is_teacher_manager = models.BooleanField(default=False)
    is_teacher_club = models.BooleanField(default=False)
    is_student_manager = models.BooleanField(default=False)
    is_club_manager = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)

    user_profile = models.ForeignKey(ClubUserProfile, null=True, blank=True, on_delete=models.DO_NOTHING)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = StudentClubUserManager()

    def __str__(self):
        return "用户" + self.phone_number


