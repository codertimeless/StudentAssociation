import random

import factory
from faker import Faker
from accounts.models.studentclub_user import StudentClubUser


faker = Faker()


class StudentClubUserFactory(factory.django.DjangoModelFactory):
    class Meta(object):
        model = StudentClubUser

    is_active = True
    password = "admintest"

    @factory.lazy_attribute
    def phone_number(self):
        return str(random.randint(10000, 99999))
