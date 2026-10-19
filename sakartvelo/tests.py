from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from sakartvelo.models import Category, Product

User = get_user_model()


class SakartveloShopTests(TestCase):

    def setUp(self):
        # Створюємо тестового користувача для перевірки автентифікації
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword123"
        )

        # Створюємо тестові категорії (використовуючи правильне поле 'title')
        self.category_1 = Category.objects.create(title="Cheese")
        self.category_2 = Category.objects.create(title="Wine")

        # Створюємо активні та неактивні товари для
        # перевірки видимості та фільтрації
        self.product_active_1 = Product.objects.create(
            title="Gouda Cheese",
            price=150.00,
            category=self.category_1,
            is_active=True
        )
        self.product_active_2 = Product.objects.create(
            title="Brie Cheese",
            price=200.00,
            category=self.category_1,
            is_active=True
        )
        self.product_inactive = Product.objects.create(
            title="Old Wine",
            price=500.00,
            category=self.category_2,
            is_active=False
        )

        # URL для головної сторінки магазину відповідно до вашого urls.py
        self.shop_url = reverse("sakartvelo:index")
        self.shop_grid_url = reverse("sakartvelo:shop-grid")

    def test_authentication_required(self):
        """Перевірка того, що неавторизований користувач
        перенаправляється на сторінку логіну (LoginRequiredMixin)"""
        detail_url = reverse(
            "sakartvelo:product-detail",
            kwargs={"pk": self.product_active_1.pk}
        )
        response = self.client.get(detail_url)
        # Очікуємо редирект (код 302) на сторінку логіну
        self.assertEqual(response.status_code, 302)

        # Тепер авторизуємось і перевіримо доступ
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)

    def test_active_and_inactive_product_visibility(self):
        """Перевірка того, що активні товари відображаються,
        а неактивні видають 404"""
        self.client.login(
            username="testuser",
            password="testpassword123")

        # Активний товар має бути доступний
        active_url = reverse(
            "sakartvelo:product-detail",
            kwargs={"pk": self.product_active_1.pk}
        )
        response = self.client.get(active_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gouda Cheese")

        # Неактивний товар повинен повертати 404 Not
        # Found (завдяки перевизначеному get_queryset)
        inactive_url = reverse(
            "sakartvelo:product-detail",
            kwargs={"pk": self.product_inactive.pk}
        )
        response = self.client.get(inactive_url)
        self.assertEqual(response.status_code, 404)

    def test_product_search(self):
        """Перевірка роботи пошуку за параметром 'q' на сторінці shop-grid"""
        self.client.login(
            username="testuser",
            password="testpassword123"
        )

        response = self.client.get(self.shop_grid_url, {"q": "Gouda"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gouda Cheese")
        self.assertNotContains(response, "Brie Cheese")

    def test_category_filtering(self):
        """Перевірка фільтрації товарів за категорією
        через параметри або окремий маршрут"""
        self.client.login(
            username="testuser",
            password="testpassword123")

        # Перевірка фільтрації через GET-параметр на shop-grid
        response = self.client.get(
            self.shop_grid_url,
            {"category": self.category_1.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gouda Cheese")
        self.assertContains(response, "Brie Cheese")

        # Перевірка окремого маршруту категорії (CategoryProductListView)
        category_url = reverse(
            "sakartvelo:category_products",
            kwargs={"category_id": self.category_1.id}
        )
        response = self.client.get(category_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gouda Cheese")

    def test_product_sorting(self):
        """Перевірка сортування товарів за ціною
        (від дешевих до дорогих і навпаки)"""
        self.client.login(
            username="testuser",
            password="testpassword123"
        )

        # Сортування: від дешевих до дорогих ('price')
        response = self.client.get(self.shop_grid_url, {"sort": "price"})
        self.assertEqual(response.status_code, 200)
        products = list(response.context["page_obj"])
        # Перевіряємо порядок: першим має йти дешевкий товар (150.00)
        self.assertEqual(products[0].price, 150.00)

        # Сортування: від дорогих до дешевих ('-price')
        response = self.client.get(self.shop_grid_url, {"sort": "-price"})
        self.assertEqual(response.status_code, 200)
        products = list(response.context["page_obj"])
        self.assertEqual(products[0].price, 200.00)

    def test_pagination(self):
        """Перевірка того, що пагінація працює і
        коректно приймає параметри"""
        # Створимо додатково товари, щоб загальна кількість
        # перевищила ліміт (9 товарів на сторінку)
        for i in range(15):
            Product.objects.create(
                title=f"Cheese Extra {i}",
                price=100.0 + i,
                category=self.category_1,
                is_active=True
            )

        self.client.login(username="testuser", password="testpassword123")

        # Запит на другу сторінку shop-grid
        response = self.client.get(self.shop_grid_url, {"page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["page_obj"].has_previous())