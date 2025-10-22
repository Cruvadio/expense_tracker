from django.contrib import admin

from .models import Transaction, Category

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'date', 'category', 'description')
    search_fields = ('description',)
    list_filter = ('date', 'category')
    empty_value_display = '-пусто-'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'

