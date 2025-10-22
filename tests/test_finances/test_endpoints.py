import pytest
from rest_framework import status

from finances.models import Transaction, Category

pytestmark = pytest.mark.django_db


class TestCategoryEndpoints:
    endpoint = '/api/categories/'

    @pytest.mark.parametrize(
        'client_fixture, expected_status',
        (
                (pytest.lazy_fixture('auth_client'),
                        status.HTTP_403_FORBIDDEN),
                (pytest.lazy_fixture('auth_admin_client'),
                 status.HTTP_201_CREATED),
        ))
    def test_create_category(self, client_fixture, expected_status):
        client, _ = client_fixture
        data = {'name': 'Utilities'}
        response = client.post(self.endpoint, data)
        assert response.status_code == expected_status
        if expected_status == status.HTTP_201_CREATED:
            assert response.data['name'] == 'Utilities'

    @pytest.mark.skip
    def test_create_category_unauthenticated(self, api_client):
        data = {'name': 'Utilities'}
        response = api_client.post(self.endpoint, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_categories(self, auth_client, create_category):
        client, _ = auth_client
        create_category(name='Groceries')
        create_category(name='Rent')
        response = client.get(self.endpoint)
        assert response.status_code == 200
        assert len(response.data) >= 2

    def test_retrieve_category(self, auth_client, create_category):
        client, _ = auth_client
        category = create_category(name='Entertainment')
        response = client.get(f'{self.endpoint}{category.id}/')
        assert response.status_code == 200
        assert response.data['name'] == 'Entertainment'

    @pytest.mark.parametrize(
        'client_fixture, expected_status',
        (
                (pytest.lazy_fixture('auth_client'),
                 status.HTTP_403_FORBIDDEN),
                (pytest.lazy_fixture('auth_admin_client'),
                 status.HTTP_200_OK),
        ))
    def test_update_category(self, client_fixture, expected_status,
                             create_category):
        client, _ = client_fixture
        category = create_category(name='Old Name')
        data = {'name': 'New Name'}
        response = client.put(f'{self.endpoint}{category.id}/', data)
        assert response.status_code == expected_status
        if expected_status == status.HTTP_200_OK:
            assert response.data['name'] == 'New Name'

    @pytest.mark.parametrize(
        'client_fixture, expected_status',
        (
                (pytest.lazy_fixture('auth_client'),
                 status.HTTP_403_FORBIDDEN),
                (pytest.lazy_fixture('auth_admin_client'),
                 status.HTTP_204_NO_CONTENT),
        ))
    def test_delete_category(self, client_fixture, expected_status,
                             create_category):
        client, _ = client_fixture
        category = create_category(name='To Be Deleted')
        response = client.delete(f'{self.endpoint}{category.id}/')
        assert response.status_code == expected_status
        if expected_status == status.HTTP_204_NO_CONTENT:
            assert not Category.objects.filter(id=category.id).exists()
        else:
            assert Category.objects.filter(id=category.id).exists()


class TestTransactionEndpoints:
    endpoint = '/api/transactions/'

    def test_create_transaction(self, auth_client, create_category):
        client, _ = auth_client
        category = create_category(name='Groceries')
        data = {
            'amount': 150.75,
            "transaction_type": "income",
            'date': '2024-06-15',
            'category': category.id,
            'description': 'Weekly grocery shopping'
        }
        response = client.post(self.endpoint, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['amount'] == '150.75'
        assert response.data['category'] == category.id

    def test_list_transactions(self, auth_client, create_transaction):
        client, user = auth_client
        create_transaction(amount=50.00, description='Transaction 1',
                           owner=user)
        create_transaction(amount=75.25, description='Transaction 2',
                           owner=user)
        response = client.get(self.endpoint)
        results = response.data['results']
        assert response.status_code == status.HTTP_200_OK
        assert len(results) >= 2

    def test_retrieve_transaction_for_owner(self, auth_client,
                                            create_transaction):
        client, user = auth_client
        transaction = create_transaction(amount=100.00,
                                         description='Test Transaction',
                                         owner=user)
        response = client.get(f'{self.endpoint}{transaction.id}/')
        assert response.status_code == 200
        assert response.data['description'] == 'Test Transaction'

    def test_update_transaction_for_owner(self, auth_client,
                                          create_transaction, create_category):
        client, user = auth_client
        transaction = create_transaction(amount=200.00,
                                         description='Old Description',
                                         owner=user)
        new_category = create_category(name='Rent')
        data = {
            'amount': 250.00,
            "transaction_type": "income",
            'date': transaction.date,
            'category': new_category.id,
            'description': 'Updated Description'
        }
        response = client.put(f'{self.endpoint}{transaction.id}/', data)
        assert response.status_code == 200
        assert response.data['amount'] == '250.00'
        assert response.data['description'] == 'Updated Description'
        assert response.data['category'] == new_category.id

    def test_delete_transaction_for_owner(self, auth_client,
                                          create_transaction):
        client, user = auth_client
        transaction = create_transaction(amount=300.00,
                                         description='To Be Deleted',
                                         owner=user)
        response = client.delete(f'{self.endpoint}{transaction.id}/')
        assert response.status_code == 204
        assert not Transaction.objects.filter(id=transaction.id)

    def test_delete_transaction_not_owner(self, auth_client,
                                          create_transaction, create_user):
        client, user = auth_client
        other_user = create_user(username='otheruser')
        transaction = create_transaction(amount=300.00,
                                         description='Not My Transaction',
                                         owner=other_user)
        response = client.delete(f'{self.endpoint}{transaction.id}/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert Transaction.objects.filter(id=transaction.id).exists()

    def test_update_transaction_not_owner(self, auth_client,
                                          create_transaction, create_user,
                                          create_category):
        client, user = auth_client
        other_user = create_user(username='otheruser')
        transaction = create_transaction(amount=200.00,
                                         description='Other User Transaction',
                                         owner=other_user)
        new_category = create_category(name='Rent')
        data = {
            'amount': 250.00,
            "transaction_type": "income",
            'date': transaction.date,
            'category': new_category.id,
            'description': 'Attempted Update'
        }
        response = client.put(f'{self.endpoint}{transaction.id}/', data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        transaction.refresh_from_db()
        assert transaction.amount == 200.00
        assert transaction.description == 'Other User Transaction'
        assert transaction.category != new_category

    def test_retrieve_transaction_not_owner(self, auth_client,
                                            create_transaction, create_user):
        client, user = auth_client
        other_user = create_user(username='otheruser')
        transaction = create_transaction(amount=100.00,
                                         description='Other User Transaction',
                                         owner=other_user)
        response = client.get(f'{self.endpoint}{transaction.id}/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
