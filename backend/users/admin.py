from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'bio')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')
    ordering = ('username',)
    empty_value_display = '-пусто-'
    list_editable = ('is_active', 'is_staff')