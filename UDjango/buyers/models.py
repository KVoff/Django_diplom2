# buyers/models.py
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        Group, Permission)
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from registration.models import \
    BuyerManager  # Убедитесь, что BuyerManager реализован для кастомной модели пользователя


class Address(models.Model):
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.street}, {self.house_number}"


class Buyer(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    special_notes = models.TextField(blank=True, null=True)
    phone_number = models.CharField(
        max_length=12, unique=True,
        validators=[
            RegexValidator(
                regex=r'^\+7\d{10}$',
                message="Введите корректный номер телефона (например, +79991234567)."
            )
        ]
    )
    password = models.CharField(max_length=128)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    email = models.EmailField(unique=True, blank=True, null=True)
    addresses = models.ManyToManyField(Address, related_name="buyers",
                                       blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Связи с группами и правами
    groups = models.ManyToManyField(
        Group,
        related_name='buyer_set',  # Указываем уникальное имя для связи
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='buyer_permissions',  # Указываем уникальное имя для связи
        blank=True
    )

    objects = BuyerManager()  # Обеспечьте, что BuyerManager настроен правильно для модели пользователя

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.phone_number}"

    def clean(self):
        # Проверка на корректность даты рождения
        if self.date_of_birth and self.date_of_birth > timezone.now().date():
            raise ValidationError("Дата рождения не может быть в будущем.")

    def to_dict(self):
        return {
            "id": self.pk,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "special_notes": self.special_notes,
            "phone_number": self.phone_number,
            "email": self.email,
            "address": [
                {"street": addr.street, "house_number": addr.house_number} for
                addr in self.addresses.all()
            ],
        }
