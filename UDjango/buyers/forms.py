# buyers/forms.py
from datetime import date
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Buyer, Address
from django.db import connection


class BuyerForm(forms.ModelForm):
    # Фильтруем адреса, показывая только те, что принадлежат текущему покупателю
    # addresses = forms.ModelMultipleChoiceField(
    #     queryset=Address.objects.none(),  # Пустой queryset по умолчанию
    #     required=False,
    #     widget=forms.SelectMultiple,
    # )

    # Поля для ввода нового адреса
    street = forms.CharField(
        label='Улица',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Введите улицу'})
    )
    house_number = forms.CharField(
        label='Номер дома',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Введите номер дома'})
    )

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(),
        required=True
    )

    password_confirmation = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput(),
        required=True
    )

    class Meta:
        model = Buyer
        fields = ['first_name', 'last_name', 'date_of_birth', 'special_notes',
                  'phone_number', 'email', 'addresses', 'street',
                  'house_number', 'password']
        widgets = {
            'date_of_birth': forms.TextInput(
                attrs={'placeholder': 'ГГГГ-ММ-ДД'}),
            'special_notes': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
            'phone_number': forms.TextInput(
                attrs={'placeholder': '+79991234567'}),
        }

        error_messages = {
            'date_of_birth': {'invalid': 'Формат ГГГГ-ММ-ДД.'},
            'phone_number': {
                'invalid': 'Формат +79991234567'}
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Если покупатель уже существует (обновление), делаем пароли необязательными
        if self.instance.pk:
            self.fields['password'].required = False
            self.fields['password_confirmation'].required = False



            self.fields['addresses'].queryset = self.instance.addresses.all()
            # Убираем поле "addresses" из формы, если у покупателя нет адресов
            if not self.instance.addresses.exists():
                self.fields.pop('addresses')



    def clean_password(self):
        password = self.cleaned_data.get('password')

        # Если пользователь не ввёл новый пароль и это обновление, возвращаем None
        if not password and self.instance.pk:
            return None
        return password

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        # Проверяем подтверждение пароля только если введён новый пароль
        if password:  # Проверка выполняется только если поле 'password' заполнено
            if not password_confirmation:
                raise ValidationError(
                    "Подтвердите пароль.")
            if password != password_confirmation:
                raise ValidationError("Пароли не совпадают.")

        return password_confirmation

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        today = timezone.now().date()
        max_age_date = date(today.year - 120, today.month, today.day)

        if date_of_birth:
            if date_of_birth > today:
                raise ValidationError("Дата рождения не может быть в будущем.")
            if date_of_birth < max_age_date:
                raise ValidationError(
                    "Дата рождения не может быть ранее 120 лет назад.")

        return date_of_birth

    def save(self, commit=True):
        buyer = super().save(commit=False)

        try:
            # Обработка нового пароля
            password = self.cleaned_data.get('password')
            if password:
                # Устанавливаем новый хэшированный пароль, если он введён
                buyer.set_password(password)
            elif self.instance.pk:
                # Загружаем текущий пароль из базы данных, если новый пароль не введён
                current_password = type(self.instance).objects.get(
                    pk=self.instance.pk).password
                buyer.password = current_password
            else:
                # Если нет ни текущего, ни нового пароля, выдаём ошибку
                raise ValidationError(
                    "Пароль обязателен.")

            if commit:
                buyer.save()

            # Получаем новый адрес, если он был введен
            new_street = self.cleaned_data.get('street')
            new_house_number = self.cleaned_data.get('house_number')

            # Если введен новый адрес, создаем и добавляем его
            if new_street and new_house_number:
                address, created = Address.objects.get_or_create(
                    street=new_street,
                    house_number=new_house_number)
                print(f"Address created: {address}")  # Отладка

                buyer.addresses.add(address)

            # Добавляем адреса из формы
            if 'addresses' in self.cleaned_data:
                buyer.addresses.add(*self.cleaned_data['addresses'])


            if commit:
                buyer.save()

            return buyer

        except Exception as e:
            print(f"Error during save: {e}")
            raise e


class BuyerLoginForm(forms.Form):
    phone_number = forms.CharField(label="Номер телефона", max_length=12)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get("phone_number")
        password = cleaned_data.get("password")

        if phone_number and password:
            user = authenticate(phone_number=phone_number, password=password)
            if user is None:
                raise forms.ValidationError(
                    "Неправильный номер телефона или пароль.")
            elif not user.is_active:
                raise forms.ValidationError("Ваш аккаунт отключен.")

        return cleaned_data
