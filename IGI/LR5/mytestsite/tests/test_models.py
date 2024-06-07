from django.test import TestCase
from django.contrib.auth.models import User
from mytestsite.agency.models import Client, PromoCode, Order


class ClientModelTest(TestCase):

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='password')

        # Создаем несколько тестовых промокодов
        self.promo_code1 = PromoCode.objects.create(code='CODE1', discount_percentage=10)
        self.promo_code2 = PromoCode.objects.create(code='CODE2', discount_percentage=15)

        # Создаем клиента
        self.client = Client.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            address='123 Main St',
            birth_date='2000-01-01',
            belarus_phone_number='+375123456789'
        )

        # Привязываем промокоды к клиенту
        self.client.promo_codes.add(self.promo_code1)
        self.client.promo_codes.add(self.promo_code2)

        # Создаем несколько тестовых заказов для клиента
        self.order1 = Order.objects.create(client=self.client, final_price=100)
        self.order2 = Order.objects.create(client=self.client, final_price=150)
        self.order3 = Order.objects.create(client=self.client, final_price=200)

    def test_total_orders(self):
        self.assertEqual(self.client.total_orders(), 3)

    def test_total_spent(self):
        self.assertEqual(self.client.total_spent(), 450)  # 100 + 150 + 200 = 450
