from datetime import timedelta

from django.utils import timezone
from django.db.models import Sum, Case, When, F, DecimalField, QuerySet


def get_analytics(queryset: QuerySet) -> dict:
    total_income = \
        queryset.filter(transaction_type='income').aggregate(
            total=Sum('amount'))[
            'total'] or 0
    total_expense = \
        queryset.filter(transaction_type='expense').aggregate(
            total=Sum('amount'))[
            'total'] or 0

    # Баланс
    balance = total_income - total_expense

    # По категориям
    by_category = (
        queryset.values('category__name')
        .annotate(
            income=Sum(
                Case(
                    When(transaction_type='income', then=F('amount')),
                    default=0, output_field=DecimalField()
                )
            ),
            expense=Sum(
                Case(
                    When(transaction_type='expense', then=F('amount')),
                    default=0, output_field=DecimalField()
                )
            )
        )
        .annotate(
            balance=F('income') - F('expense')
        )
        .order_by('balance')
    )

    # Динамика по дням (за последние 30 дней)
    last_30 = timezone.now().today() - timedelta(days=30)
    daily = (
        queryset.filter(date__gte=last_30)
        .values('date__date')
        .annotate(
            income=Sum(
                Case(
                    When(transaction_type='income', then=F('amount')),
                    default=0, output_field=DecimalField()
                )
            ) - Sum(
                Case(
                    When(transaction_type='expense', then=F('amount')),
                    default=0, output_field=DecimalField()
                )
            )
        )
    )

    return {
        'income': total_income,
        'expense': total_expense,
        'balance': balance,
        'by_category': list(by_category),
        'daily': list(daily)
    }


def beutify_analytics(analytics) -> str:
    categories = []
    for category in analytics['by_category']:
        categories.append(
            f'''Категория: {category['category__name']}
                доход: {category['income']},
                расход: {category["expense"]}'''
        )
    categories_str = '\n'.join(categories)
    daily = []
    for day in analytics['daily']:
        daily.append(f'День: {day["date__date"]} чистый доход: {day["income"]}')
    daily_str = '\n'.join(daily)
    return f"""
    Ваши доходы за неделю: {analytics["income"]}
    Ваши расходы за неделю: {analytics["expense"]}
    Ваш баланс: {analytics["balance"]}
    Топ самых затратных категорий:\n{categories_str}
    Ежедневный доход:\n {daily_str}
    """



