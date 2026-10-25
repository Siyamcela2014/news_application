"""Admin configuration for the News Application."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Article, Publisher, Newsletter


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("News Application Role", {"fields": ("role",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("News Application Role", {"fields": ("role",)}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Article)
admin.site.register(Publisher)
admin.site.register(Newsletter)
