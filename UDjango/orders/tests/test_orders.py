from django.test import TestCase
from django.core.exceptions import ValidationError
from buyers.models import Buyer, Address  # Добавляем Address
from products.models import Product
from orders.models import Order, OrderItem


class OrderModelTestCase(TestCase):

    def setUp(self):
        # Создаем покупателя и продукт для тестов
        self.buyer = Buyer.objects.create(
            first_name='Брюс', last_name='Ли', phone_number='+79991234567',
            email='bl@example.com', date_of_birth='2000-10-11'
        )
        self.product1 = Product.objects.create(
            name='Product 1', description='Product for testing', price=50.00,
            count=10
        )
        self.product2 = Product.objects.create(
            name='Product 2', description='Another product', price=20.00,
            count=5
        )

        # Создаем адреса
        self.address1 = Address.objects.create(
            street='Lenina',
            house_number='15'
        )
        self.address2 = Address.objects.create(
            street='Stalina',
            house_number='13'
        )

        # Привязываем адреса к покупателю
        self.buyer.addresses.add(self.address1, self.address2)

    def test_create_order(self):
        # Тест на создание заказа
        order = Order.objects.create(buyer=self.buyer)
        self.assertEqual(order.buyer, self.buyer)
        self.assertEqual(order.price, 0)  # Начальная цена по умолчанию 0

    def test_order_item_creation_and_stock_update(self):
        # Тест на создание OrderItem и обновление количества продукта
        order = Order.objects.create(buyer=self.buyer)
        order_item = OrderItem.objects.create(order=order,
                                              product=self.product1,
                                              quantity=3)

        # Проверка, что количество продукта уменьшилось
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.count, 7)
        self.assertEqual(order_item.quantity, 3)

    def test_order_total_price_calculation(self):
        # Тест на подсчет общей стоимости заказа
        order = Order.objects.create(buyer=self.buyer)
        OrderItem.objects.create(order=order, product=self.product1,
                                 quantity=2)
        OrderItem.objects.create(order=order, product=self.product2,
                                 quantity=1)

        order.calculate_total_price()  # Подсчитываем итоговую цену заказа
        self.assertEqual(order.price, 120.00)  # (50 * 2) + (20 * 1) = 120

    def test_order_item_quantity_validation(self):
        # Тест на валидацию количества позиций заказа
        order = Order.objects.create(buyer=self.buyer)
        with self.assertRaises(ValidationError):
            OrderItem.objects.create(order=order, product=self.product2,
                                     quantity=6)  # Превышение доступного количества

    def test_order_to_dict_method_with_delivery_address(self):
        # Тест на метод to_dict с учетом адреса доставки
        order = Order.objects.create(buyer=self.buyer)
        order_item = OrderItem.objects.create(order=order,
                                              product=self.product1,
                                              quantity=2)
        order.calculate_total_price()

        # Присваиваем объект Address как delivery_address
        order.delivery_address = self.address1  # Указываем конкретный адрес
        order.save()

        expected_dict = {
            "order_id": order.id,
            "created_at": order.created_at,
            "price": str(order.price),
            "order_items": [
                {
                    "product_id": self.product1.id,
                    "product_name": self.product1.name,
                    "quantity": 2
                }
            ],
            "delivery_address": str(self.address1)  # Используем __str__ для вывода адреса
        }
        self.assertEqual(order.to_dict(), expected_dict)

    def test_order_to_dict_method_without_delivery_address(self):
        # Тест на метод to_dict без адреса доставки
        order = Order.objects.create(buyer=self.buyer)
        order_item = OrderItem.objects.create(order=order,
                                              product=self.product1,
                                              quantity=2)
        order.calculate_total_price()

        # Если delivery_address не указан, то выводим дефолтное сообщение
        expected_dict = {
            "order_id": order.id,
            "created_at": order.created_at,
            "price": str(order.price),
            "order_items": [
                {
                    "product_id": self.product1.id,
                    "product_name": self.product1.name,
                    "quantity": 2
                }
            ],
            "delivery_address": "Адрес доставки не указан"
        }
        self.assertEqual(order.to_dict(), expected_dict)
