from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('wallet_address', 'id', 'is_staff', 'is_active',)
    list_filter = ('wallet_address', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('wallet_address', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('wallet_address', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('wallet_address',)
    ordering = ('wallet_address',)


admin.site.register(CustomUser, CustomUserAdmin)