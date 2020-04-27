from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


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
        user.staff = True
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
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user
    
    def normalize_number(self, phone_number):
        if isinstance(phone_number, str):
            return phone_number
        

class StudentClubUser(AbstractUser):
    phone_number = models.CharField(max_length=150, unique=True)

    default_nickname = "用户"
    nickname = models.CharField(max_length=10, default=default_nickname, null=True, blank=True)
    email = models.CharField(null=True, blank=True, max_length=30)

    active = models.BooleanField(default=True)

    # admin permissions
    teacher_manager = models.BooleanField(default=False)
    teacher_club = models.BooleanField(default=False)
    student_manager = models.BooleanField(default=False)
    club_manager = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = StudentClubUserManager()

    def get_is_active(self):
        return self.active

    def __str__(self):
        return "用户" + self.phone_number


