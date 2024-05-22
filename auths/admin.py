from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = [
        "username",
        "email",
        "is_active",
        "is_superuser",
    ]


admin.site.register(CustomUser, CustomUserAdmin)
