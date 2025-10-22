import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_register_user(api_client):
    url = reverse('auth-register')
    data = {
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'pass1234'
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in response.data


@pytest.mark.django_db
def test_login_user(api_client, create_user):
    user = create_user()
    url = reverse('token_obtain_pair')
    response = api_client.post(url, {
        'username': user.username,
        'password': 'pass1234'
    })
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
