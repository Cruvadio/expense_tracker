import pytest
from rest_framework import status


@pytest.mark.django_db
def test_profile_access_requires_auth(api_client):
    response = api_client.get('/api/auth/profile/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_profile_retrieval(auth_client):
    client, user = auth_client
    response = client.get('/api/auth/profile/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['username'] == user.username
