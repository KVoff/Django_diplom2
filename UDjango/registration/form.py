from django import forms

from django.contrib.auth.forms import UserCreationForm
from buyers.models import Buyer


class BuyerRegistrationForm(UserCreationForm):
    # Переопределение поля password2 (подтверждение пароля)
    password2 = forms.CharField(
        label="Confirm",  # Переименуем метку, если нужно
        # help_text="Введите тот же пароль, что и выше, для подтверждения.",
        # Новый текст
        widget=forms.PasswordInput,
    )

    class Meta:
        model = Buyer
        fields = ['phone_number', 'password1', 'password2', 'first_name']


