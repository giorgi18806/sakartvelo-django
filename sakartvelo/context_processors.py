from .models import Category


def global_categories(request):
    return {
        "categories": Category.objects.filter(is_active=True)
    }
