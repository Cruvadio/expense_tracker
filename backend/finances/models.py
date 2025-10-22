from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2,
                                 verbose_name='Сумма')
    transaction_type = models.CharField(max_length=7,
                                        choices=TRANSACTION_TYPES,
                                        verbose_name='Тип транзакции')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='transactions',
        verbose_name='Категория'
    )
    date = models.DateTimeField(default=timezone.now,
                                verbose_name='Дата и время')
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Описание')
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='transactions',
        verbose_name='Владелец'
    )

    class Meta:
        ordering = ['-date']
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

    def __str__(self):
        return f"{self.transaction_type.capitalize()} of {self.amount} on {self.date.strftime('%Y-%m-%d')}"
