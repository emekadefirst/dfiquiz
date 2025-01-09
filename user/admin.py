from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ["email", "username", "is_staff", "is_active", "created_at"]
    list_filter = ["is_staff", "is_active"]
    search_fields = ["email", "username", "phone_number"]
    ordering = ["created_at"]
    readonly_fields = ["id", "created_at"]

    # Fieldsets for detailed view
    fieldsets = [
        (None, {"fields": ["email", "username", "phone_number", "password"]}),
        ("Permissions", {"fields": ["is_staff", "is_active", "is_superuser"]}),
        ("Important Dates", {"fields": ["last_login", "created_at"]}),
    ]

    # Fields used for creating a new user
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "username",
                    "phone_number",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ],
            },
        ),
    ]


admin.site.register(User, UserAdmin)
