import pytest
from .factories  import TransactionFactory, CategoryFactory


@pytest.fixture
def create_category():
    def _create_category(**kwargs):
        return CategoryFactory(**kwargs)
    return _create_category
@pytest.fixture
def create_transaction():
    def _create_transaction(**kwargs):
        return TransactionFactory(**kwargs)
    return _create_transaction

@pytest.fixture
def make_categories():
    categories = [
        CategoryFactory(name='Food'),
        CategoryFactory(name='Rent'),
        CategoryFactory(name='Utilities'),
    ]
    return categories

@pytest.fixture
def make_transactions(categories):
    transactions = [
        TransactionFactory(amount=50.00, transaction_type='expense',
                           category=categories[0],
                           description='Grocery shopping'),
        TransactionFactory(amount=1500.00, transaction_type='income',
                           category=categories[1],
                           description='Monthly rent payment'),
        TransactionFactory(amount=100.00, transaction_type='expense',
                           category=categories[2],
                           description='Electricity bill payment'),
    ]
    return transactions

@pytest.fixture
def batch_transactions(create_transaction):
    def _batch_transactions(number):
        return [create_transaction() for _ in range(number)]
    return _batch_transactions