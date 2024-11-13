# employee/forms.py

from django import forms
from django.conf import settings
from django.contrib.auth import authenticate

from .models import EmployeeProfile


class EmployeeLoginForm(forms.Form):
    username = forms.CharField(label="Логин", max_length=150)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Неправильный логин или пароль.")
            elif not user.is_staff:
                raise forms.ValidationError(
                    "Нет прав доступа для сотрудников.")

        return cleaned_data


# # employee/forms.py


class EmployeeProfileAdminForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ('user', 'position', 'department', 'hire_date')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Фильтруем пользователей только для сотрудников
    #     self.fields['user'].queryset = settings.AUTH_USER_MODEL.objects.filter(
    #         is_staff=True)

# 1 вариант

# from django import forms
# from django.contrib.auth import get_user_model
# from .models import EmployeeProfile
#
#
# class EmployeeProfileAdminForm(forms.ModelForm):
#     class Meta:
#         model = EmployeeProfile
#         fields = ('user', 'position', 'department', 'hire_date')
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Фильтруем пользователей только для сотрудников
#         self.fields['user'].queryset = get_user_model().objects.filter(
#             is_staff=True)
