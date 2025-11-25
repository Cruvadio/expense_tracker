import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db

def test_pagination(auth_client, create_user, create_category, batch_transactions):
    client, user = auth_client
    batch_transactions(15)
    url = reverse('transaction-list') + '?page=2'
    response = client.get(url)

    assert response.status_code == 200
    assert 'results' in response.data
    assert response.data['count'] == 15
    assert len(response.data['results']) == 5