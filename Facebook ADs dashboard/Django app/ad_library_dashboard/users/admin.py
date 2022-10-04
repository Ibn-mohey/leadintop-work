from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser
# Register your models here.

# admin.site.register(CustomUser)

"""Integrate with admin module."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy  as _

from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','name'),
        }),
    )
    list_display = ('email', 'name', 'is_staff','is_active')
    search_fields = ('email',)
    ordering = ('email',)