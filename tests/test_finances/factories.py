import factory
from django.utils import timezone

from tests.test_users.factories import UserFactory


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'finances.Category'

    name = factory.Faker('word')


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'finances.Transaction'

    amount = factory.Faker('pydecimal', left_digits=4, right_digits=2,
                           positive=True)
    transaction_type = factory.Iterator(['income', 'expense'])
    category = factory.SubFactory(CategoryFactory)
    date = factory.Faker('date_time_this_year', before_now=True,
                         after_now=False,
                         tzinfo=timezone.get_current_timezone())
    description = factory.Faker('sentence')
    owner = factory.SubFactory(UserFactory)
