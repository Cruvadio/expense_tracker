from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import CategoriesViewSet, TransactionsViewSet
from .views_analytics import AnalyticsView, WeeklyReportViewSet

router = DefaultRouter()
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'transactions', TransactionsViewSet, basename='transactions')
router.register(r'weekly_reports', WeeklyReportViewSet,
                basename='weekly_reports')
urlpatterns = [
    path('', include(router.urls)),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
]
