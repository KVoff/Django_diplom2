from django.test import TestCase
from buyers.models import Buyer
import time


class RealDatabaseTest(TestCase):
    def setUp(self):
        # Измеряем время создания 100,000 экземпляров модели Buyer
        start_time = time.time()

        # Создание 100,000 экземпляров модели Buyer
        self.buyers = []
        for i in range(100_000):
            buyer = Buyer(
                first_name=f"Имя{i}",
                last_name=f"Фамилия{i}",
                date_of_birth="2000-09-10",
                phone_number=f"+79991234567{i}",
                email=f"buyer{i}@example.com"
            )
            self.buyers.append(buyer)

        # Сохраняем созданных покупателей
        Buyer.objects.bulk_create(self.buyers)

        creation_time = time.time() - start_time
        print(f"Время создания покупателей: {creation_time:.2f} секунд")

    def tearDown(self):
        # Удаляем всех покупателей после теста
        Buyer.objects.all().delete()

    def test_crud_operations(self):
        # Измеряем время выполнения обновления
        start_time = time.time()
        for buyer in Buyer.objects.all():
            buyer.first_name += "_upd"
            buyer.save()
        update_time = time.time() - start_time
        print(f"Время выполнения обновления: {update_time:.2f} секунд")

        # Измеряем время выполнения чтения
        start_time = time.time()
        all_buyers = list(Buyer.objects.all())
        read_time = time.time() - start_time
        print(f"Время выполнения чтения: {read_time:.2f} секунд")

        # Измеряем время выполнения удаления
        start_time = time.time()
        Buyer.objects.all().delete()
        delete_time = time.time() - start_time
        print(f"Время выполнения удаления: {delete_time:.2f} секунд")
