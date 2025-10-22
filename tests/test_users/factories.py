import factory

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'users.User'

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True