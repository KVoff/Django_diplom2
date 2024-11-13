# accounts/auth_backends.py

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from buyers.models import Buyer
from employee.models import EmployeeProfile

class EmployeeBackend(BaseBackend):
    """
    Аутентификационный бэкенд для сотрудников, использующий логин и пароль.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()  # Получаем модель пользователя, которая используется для Employee
        try:
            user = User.objects.get(username=username)
            if user.check_password(password) and user.is_staff:
                return user
        except ObjectDoesNotExist:
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class BuyerBackend(BaseBackend):
    """
    Аутентификационный бэкенд для покупателей, использующий номер телефона и пароль.
    """
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        try:
            buyer = Buyer.objects.get(phone_number=phone_number)
            if buyer.check_password(password) and buyer.is_active:
                return buyer
        except Buyer.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Buyer.objects.get(pk=user_id)
        except Buyer.DoesNotExist:
            return None
