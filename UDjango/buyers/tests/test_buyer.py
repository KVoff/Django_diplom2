from django.test import TestCase
from buyers.models import Buyer, Address
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date

class BuyerModelTestCase(TestCase):

    def setUp(self):
        # Создание адреса для покупателя
        self.address = Address.objects.create(street='Stroiteley',
                                              house_number='21')

    def test_create_buyer(self):
        # Тест на создание покупателя
        buyer = Buyer.objects.create(
            first_name='Брюс',
            last_name='Ли',
            date_of_birth=date(2000, 9, 8),
            phone_number='+79991234567',
            email='bl@example.com'
        )
        self.assertEqual(buyer.first_name, 'Брюс')
        self.assertEqual(buyer.last_name, 'Ли')
        self.assertEqual(buyer.phone_number, '+79991234567')
        self.assertEqual(buyer.email, 'bl@example.com')

    def test_buyer_string_representation(self):
        # Тест на корректное отображение строки покупателя
        buyer = Buyer(first_name='Брюс', last_name='Ли')
        self.assertEqual(str(buyer), 'Брюс Ли')

    def test_buyer_clean_method_future_date_of_birth(self):
        # Тест на валидацию даты рождения в будущем
        buyer = Buyer(
            first_name='Брюс',
            last_name='Ли',
            date_of_birth=timezone.now().date() + timezone.timedelta(days=1),
            phone_number='+79991234567',
            email='bl@example.com'
        )
        with self.assertRaises(ValidationError):
            buyer.clean()  # Запуск метода очистки для проверки валидации

    def test_buyer_to_dict(self):
        # Тест на метод to_dict
        buyer = Buyer.objects.create(
            first_name='Брюс',
            last_name='Ли',
            date_of_birth=date(2000, 9, 10),
            phone_number='+79991234567',
            email='bl@example.com'
        )
        buyer.addresses.add(self.address)  # Добавление адреса
        expected_dict = {
            'id': buyer.pk,
            'first_name': 'Брюс',
            'last_name': 'Ли',
            'date_of_birth': date(2000, 9, 10),
            'special_notes': None,
            'phone_number': '+79991234567',
            'email': 'bl@example.com',
            'address': [{'street': 'Stroiteley', 'house_number': '21'}],
        }
        self.assertEqual(buyer.to_dict(), expected_dict)

    def test_update_buyer(self):
        # Тест на обновление данных покупателя
        buyer = Buyer.objects.create(
            first_name='Брюс',
            last_name='Ли',
            date_of_birth=date(2000, 9, 10),
            phone_number='+79991234567',
            email='bl@example.com'
        )
        buyer.phone_number = '+79998887766'
        buyer.save()
        self.assertEqual(buyer.phone_number, '+79998887766')

    def test_delete_buyer(self):
        # Тест на удаление покупателя
        buyer = Buyer.objects.create(
            first_name='Брюс',
            last_name='Ли',
            date_of_birth=date(2000, 9, 10),
            phone_number='+79991234567',
            email='bl@example.com'
        )
        buyer.delete()
        with self.assertRaises(Buyer.DoesNotExist):
            Buyer.objects.get(id=buyer.id)

    def test_buyer_with_addresses(self):
        # Тест на проверку связи покупателя с адресами
        buyer = Buyer.objects.create(
            first_name='Брюс',
            last_name='Ли',
            date_of_birth=date(2000, 9, 10),
            phone_number='+79991234567',
            email='bl@example.com'
        )
        buyer.addresses.add(self.address)
        self.assertIn(self.address, buyer.addresses.all())
