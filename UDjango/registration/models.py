from django.contrib.auth.models import BaseUserManager


class BuyerManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Создает и сохраняет пользователя-покупателя с номером телефона и паролем.
        """
        if not phone_number:
            raise ValueError("Номер телефона обязателен для регистрации.")

        buyer = self.model(phone_number=phone_number, **extra_fields)
        buyer.set_password(password)
        buyer.save(using=self._db)
        return buyer
