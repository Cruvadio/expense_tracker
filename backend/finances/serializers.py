from rest_framework import serializers
from .models import Transaction, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id', 'amount', 'transaction_type', 'category',
            'date', 'description', 'owner'
        ]
        read_only_fields = ['id', 'owner']

class ScheduleSerializer(serializers.Serializer):
    time = serializers.TimeField()
    day_of_week = serializers.IntegerField()
