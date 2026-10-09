from django.contrib import admin

from .models import Category, Customer, Product


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
    list_display = ("title", "email", "phone", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title", "email", "phone")
