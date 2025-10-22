from datetime import datetime, timedelta

from core.celery_core import app
from django.core.mail import send_mail

from .utils import get_analytics, beutify_analytics
from .models import Transaction

@app.task
def notify_new_transaction(user_email, amount):
    send_mail(
        subject='New Transaction added',
        message=f'You added a new transaction to your bank account: {amount} EUR.',
        from_email='no-reply@expense-tracker.com',
        recipient_list=[user_email],
    )

@app.task
def send_weekly_report(user_id, email):
    today = datetime.today()
    week_ago = today - timedelta(days=7)
    qs = Transaction.objects.filter(owner_id=user_id, date__gte=week_ago)
    analytics = get_analytics(qs)
    send_mail(
        subject='Ваш еженедельный финансовый отчёт',
        message=beutify_analytics(analytics),
        from_email='no-reply@expense-tracker.com',
        recipient_list=[email],
    )

