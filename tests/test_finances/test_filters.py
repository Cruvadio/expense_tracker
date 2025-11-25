import pytest
from django.urls import reverse


pytestmark = pytest.mark.django_db
class TestTransactionsFilters:

    base_url = reverse('transaction-list')

    @pytest.mark.parametrize('filter_param, expected_count', [
        ('income', 1),
        ('expense', 2),
    ])
    def test_filter_transactions_by_type(self, auth_client, create_category, create_transaction, filter_param, expected_count):
        client, user = auth_client
        cat = create_category(name='Работа')
        create_transaction(category=cat, transaction_type='expense')
        create_transaction(category=cat, transaction_type='expense')
        create_transaction(category=cat, transaction_type='income')

        url = self.base_url + f'?transaction_type={filter_param}'
        response = client.get(url)

        assert response.status_code == 200
        assert len(response.data['results']) == expected_count
        assert response.data['results'][0]['type'] == filter_param


    def test_filter_transactions_by_category(self, auth_client, create_category, create_transaction):
        client, user = auth_client
        work = create_category(name='Работа')
        rest = create_category(name='Отдых')
        create_transaction(category=work)
        create_transaction(category=rest)

        url = self.base_url + f'?category={work.id}'
        response = client.get(url)

        assert response.status_code == 200
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['category'] == work.id

    def test_search_transactions_by_description(self, auth_client, create_category, create_transaction):
        client, user = auth_client
        cat = create_category(name='Работа')
        create_transaction(category=cat, description='Тестовое описание и пицца')
        create_transaction(category=cat, description='Тестовое описание 2')
        url = self.base_url + '?search=пицца'
        response = client.get(url)

        assert response.status_code == 200
        assert len(response.data['results']) == 1
        assert 'пицца' in response.data['results'][0]['description']