import random

import factory
from faker import Faker

from organizations.models import Organization

fake = Faker('ru_RU')


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    inn = factory.declarations.LazyFunction(lambda: fake.businesses_inn())
    balance = factory.declarations.LazyFunction(lambda: random.randint(0, 65535))
