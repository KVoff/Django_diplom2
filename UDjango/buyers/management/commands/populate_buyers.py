import random
import os
from datetime import datetime, timedelta

import django

# Замените 'your_project_name' на имя вашего проекта
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UDjango.settings")
django.setup()

from buyers.models import Buyer, Address


def generate_random_date(start_year=1990, end_year=2000):
    """Генерирует случайную дату между start_year и end_year."""
    start_date = datetime(year=start_year, month=1, day=1)
    end_date = datetime(year=end_year, month=12, day=31)
    random_days = random.randint(0, (end_date - start_date).days)
    return start_date + timedelta(days=random_days)

def populate_buyers():
    # Создание 10 случайных адресов
    addresses = []
    for i in range(10):
        address = Address.objects.create(
            street=f"Улица {i + 1}",
            house_number=str(random.randint(1, 100))
        )
        addresses.append(address)

    # Создание 10 случайных покупателей
    for i in range(10):
        first_name = f"Имя{i + 1}"
        last_name = f"Фамилия{i + 1}"
        date_of_birth = generate_random_date().date()
        phone_number = f"+7{random.randint(9000000000, 9999999999)}"
        email = f"buyer{i + 1}{random.randint(1000, 9999)}@example.com"
        special_notes = f"Заметка для покупателя {i + 1}"

        buyer = Buyer.objects.create(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            phone_number=phone_number,
            email=email,
            special_notes=special_notes
        )

        # Присваиваем 1-3 случайных адресов
        random_addresses = random.sample(addresses, random.randint(1, 3))
        buyer.addresses.set(random_addresses)

    print('Успешно добавлено 10 случайных записей в таблицы Buyer и Address')

if __name__ == '__main__':
    populate_buyers()
