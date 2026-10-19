from django.contrib.auth.models import AbstractUser
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    title = models.CharField(max_length=255)
    image = models.CharField(max_length=500, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["title"]

    def __str__(self):
        return self.title


class Product(TimeStampedModel):
    class Unit(models.TextChoices):
        GRAM = "g", "gram"
        KILOGRAM = "kg", "kilogram"
        PIECE = "pcs", "piece"
        PACK = "pack", "pack"
        JAR = "jar", "jar"

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name="Зображення продукту"
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, choices=Unit.choices, default=Unit.GRAM)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Customer(AbstractUser):
    title = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=32, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.title or self.username


class ContactMessage(TimeStampedModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    is_processed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Contact message"
        verbose_name_plural = "Contact messages"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.email}"
