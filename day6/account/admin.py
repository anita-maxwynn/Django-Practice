from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

class UserModelAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'is_seller', 'is_customer')
    list_filter = ('is_superuser', 'is_seller', 'is_customer')

    fieldsets = (
        ("User credentials", {'fields': ('email', 'password')}),
        ("Personal info", {'fields': ('first_name', 'last_name')}),
        ("Permissions", {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_seller', 'is_customer', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'is_seller', 'is_customer'),
        }),
    )

    search_fields = ('email',)
    ordering = ('email','id')
    filter_horizontal = ()  # ← remove default 'groups' and 'user_permissions'

admin.site.register(User, UserModelAdmin)
