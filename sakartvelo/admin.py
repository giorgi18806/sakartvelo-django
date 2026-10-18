from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, Customer, Product, ContactMessage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("title",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "unit", "is_active", "updated_at")
    list_filter = ("is_active", "category", "unit")
    search_fields = ("title", "description")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "title",
        "email",
        "phone",
        "is_active",
        "is_staff",
    )

    search_fields = (
        "username",
        "title",
        "email",
        "phone",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Customer details",
            {
                "fields": (
                    "title",
                    "phone",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Customer details",
            {
                "fields": (
                    "title",
                    "email",
                    "phone",
                )
            },
        ),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "is_processed",
        "created_at",
    )
    list_filter = ("is_processed", "created_at")
    search_fields = ("name", "email", "message")
    readonly_fields = ("created_at", "updated_at")
