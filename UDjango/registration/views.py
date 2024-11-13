from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group

from buyers.forms import BuyerForm


def register(request):
    if request.method == 'POST':
        form = BuyerForm(request.POST)
        if form.is_valid():
            # Создание покупателя, но не сохраняем в БД сразу
            buyer = form.save(commit=False)
            buyer.set_password(form.cleaned_data['password'])

            # Устанавливаем is_active в True
            buyer.is_active = True  # Активируем покупателя сразу

            buyer.save()  # Сохраняем покупателя в базе данных

            # Добавляем покупателя в группу
            group_name = 'Buyer'  # Указываем имя группы
            group = Group.objects.get(name=group_name)  # Получаем группу
            buyer.groups.add(group)  # Добавляем покупателя в группу

            # Пытаемся аутентифицировать покупателя
            buyer = authenticate(request, phone_number=form.cleaned_data[
                'phone_number'], password=form.cleaned_data['password'])

            if buyer is not None:
                login(request,
                      buyer)  # Если аутентификация прошла, выполняем вход
                request.session.save()

                # 'profile' — путь по умолчанию, если next нет
                next_url = request.GET.get('next', 'profile')
                return redirect(next_url)

            else:
                messages.error(request,
                               "Ошибка аутентификации! Проверьте данные и попробуйте снова.")
                return redirect(
                    'login')  # Перенаправление на страницу входа в случае ошибки

        else:
            messages.error(request, "Ошибка регистрации!")
    else:
        form = BuyerForm()

    return render(request, 'registration/register.html', {'form': form})

