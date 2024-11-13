import os
import django
from django.core.exceptions import ValidationError


# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UDjango.settings")
django.setup()

from buyers.models import Buyer

def pop_buyers(first_name, last_name, date_of_birth, phone_number, email):
    # Создаем экземпляр Buyer
    buyer = Buyer(
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date_of_birth,
        phone_number=phone_number,
        email=email,
    )

    try:
        # Проверка на валидность
        buyer.full_clean()
        # Сохранение в базе данных
        buyer.save()
        print(f"Покупатель {buyer} успешно добавлен.")
    except ValidationError as e:
        print(f"Ошибка валидации: {e}")

if __name__ == '__main__':
    # Пример данных для создания покупателя
    pop_buyers('test', 'test', '1990', '+7999', 'test')
