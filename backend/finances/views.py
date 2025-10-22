from rest_framework import viewsets, permissions

from .tasks import notify_new_transaction
from .models import Category, Transaction
from .serializers import CategorySerializer, TransactionSerializer


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff or request.user.is_superuser


class CategoriesViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsAdminUserOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class TransactionsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = TransactionSerializer
    filterset_fields = ['transaction_type', 'category', 'date']
    ordering_fields = ['date', 'amount']
    search_fields = ['description']

    def get_queryset(self):
        return Transaction.objects.select_related('owner').filter(
            owner=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user)
        notify_new_transaction.delay(self.request.user.email, instance.amount)

# class StatisticAPIView(generics.ListAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         return Transaction.objects.select_related('owner').filter(
#             owner=self.request.user)
#
#
#     def statistics_by_category(self, user, category, date_from, date_to):
#         filtered_qs = Transaction.objects.filter(
#             owner=user,
#             category__name=category)
#         income_total = filtered_qs.filter(
#             transaction_type='income', date__gte=date_from,
#             date__lte=date_to).aggregate(
#             total_amount=models.Sum('amount'))['total_amount'] or 0
#         expense_total = filtered_qs.filter(
#             transaction_type='expense', date__gte=date_from,
#             date__lte=date_to).aggregate(
#             total_amount=models.Sum('amount'))['total_amount'] or 0
#         return Response({
#             'category': category,
#             'income_total': income_total,
#             'expense_total': expense_total,
#             'net_total': income_total - expense_total
#         })
#
#     def get(self, request, format=None):
#         category = request.query_params.get('category')
#
#         user = request.user
#         month_ago = timezone.now() - timezone.timedelta(days=30)
#         timestamp_from = request.query_params.get('from')
#         timestamp_to = request.query_params.get('to')
#         date_from = datetime.fromtimestamp(
#             int(timestamp_from),
#             tz=timezone.tzinfo()) if timestamp_from else month_ago
#         date_to = datetime.fromtimestamp(
#             int(timestamp_to),
#             tz=timezone.tzinfo()) if timestamp_to else timezone.now()
#         if category:
#             return self.statistics_by_category(
#                 user, category, date_from, date_to)
#         transactions = Transaction.objects.filter(
#             owner=user,
#             date__gte=date_from,
#             date__lte=date_to
#         )
#
#         income_total = \
#             transactions.filter(transaction_type='income').aggregate(
#                 total=models.Sum('amount'))['total'] or 0
#         expense_total = \
#             transactions.filter(transaction_type='expense').aggregate(
#                 total=models.Sum('amount'))['total'] or 0
#
#         data = {
#             'income_total': income_total,
#             'expense_total': expense_total,
#             'net_total': income_total - expense_total
#         }
#         return Response(data)
