import random
from datetime import timezone

import factory
from faker import Faker

from operations.models import Payment

fake = Faker('ru_RU')


class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    operation_id = factory.declarations.LazyFunction(lambda: fake.uuid4())
    payer_inn = factory.declarations.LazyFunction(lambda: fake.businesses_inn())
    amount = factory.declarations.LazyFunction(lambda: random.randint(0, 65535))
    document_number = factory.declarations.LazyFunction(lambda: f'PAY-{random.randint(0, 65535)}')
    document_date = factory.declarations.LazyFunction(
        lambda: fake.date_time(tzinfo=timezone.utc).isoformat()
    )
