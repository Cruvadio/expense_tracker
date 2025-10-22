import pytest
from django.test.client import Client
from rest_framework.test import APIClient
from .test_users.factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    def _create_user(**kwargs):
        password = kwargs.pop('password', 'pass1234')
        user = UserFactory(**kwargs)
        user.set_password(password)
        user.save()
        return user
    return _create_user

@pytest.fixture
def create_admin():
    def _create_admin(**kwargs):
        password = kwargs.pop('password', 'adminpass1234')
        user = UserFactory(is_staff=True, is_superuser=True, **kwargs)
        user.set_password(password)
        user.save()
        return user
    return _create_admin



@pytest.fixture
def auth_client(api_client, create_user):
    user = create_user(username='testuser')
    response = api_client.post('/api/auth/login/', {
        'username': user.username,
        'password': 'pass1234'
    })
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client, user

@pytest.fixture
def auth_admin_client(api_client, create_admin):
    admin = create_admin(username='adminuser')
    response = api_client.post('/api/auth/login/', {
        'username': admin.username,
        'password': 'adminpass1234'
    })
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client, admin


