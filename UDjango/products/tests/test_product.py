from django.test import TestCase
from products.models import Product


class ProductModelTestCase(TestCase):

    def test_create_product(self):
        # Тест на создание продукта
        product = Product.objects.create(
            name='Test Product',
            description='Propropro',
            price=100.00,
            count=10
        )
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.description, 'Propropro')
        self.assertEqual(product.price, 100.00)
        self.assertEqual(product.count, 10)

    def test_product_string_representation(self):
        # Тест на корректное отображение строки продукта
        product = Product(name='Test Product', price=99.99)
        self.assertEqual(str(product), 'Test Product - 99.99')

    def test_product_to_dict(self):
        # Тест на метод to_dict
        product = Product.objects.create(
            name='Test Product',
            description='Product test',
            price=100.00,
            count=10
        )
        expected_dict = {
            "id": product.pk,
            "name": "Test Product",
            "description": "Product test",
            "price": 100.00,
            "count": 10,
        }
        self.assertEqual(product.to_dict(), expected_dict)

    def test_update_product(self):
        # Тест на обновление данных продукта
        product = Product.objects.create(
            name='Test Product',
            description='testtest',
            price=100.00,
            count=10
        )
        product.price = 120.00
        product.save()
        self.assertEqual(product.price, 120.00)

    def test_delete_product(self):
        # Тест на удаление продукта
        product = Product.objects.create(
            name='Test Product',
            description='testtest',
            price=100.00,
            count=10
        )
        product.delete()
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(id=product.id)

    def test_product_stock_check(self):
        # Тест на проверку количества товара на складе
        product = Product.objects.create(
            name='Product count',
            description='test count',
            price=200.00,
            count=5
        )
        self.assertEqual(product.count, 5)

