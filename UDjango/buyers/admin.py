# buyers/admin.py
from django.contrib import admin
from .models import Buyer, Address
from .forms import BuyerForm


class BuyerAdmin(admin.ModelAdmin):
    form = BuyerForm
    list_display = (
    'phone_number', 'first_name', 'last_name', 'email', 'is_active')
    search_fields = ('phone_number', 'first_name', 'last_name', 'email')
    filter_horizontal = ('groups',)

    fieldsets = (
        (None, {'fields': (
            'phone_number', 'first_name', 'last_name', 'email', 'is_active',
            'is_staff')}),
        ('Addresses', {'fields': ('addresses', 'street', 'house_number')}),
        ('Permissions', {
            'fields': ('groups',),
        }),
    )

    def save_model(self, request, obj, form, change):
        # Сохраняем пользователя
        super().save_model(request, obj, form, change)

        # Получаем значения полей street и house_number из формы
        new_street = form.cleaned_data.get('street')
        new_house_number = form.cleaned_data.get('house_number')

        # Проверка наличия новых данных для создания адреса
        if new_street and new_house_number:
            address, created = Address.objects.get_or_create(
                street=new_street,
                house_number=new_house_number
            )
            # Привязываем новый адрес к пользователю
            obj.addresses.add(address)

            print(f"Address created: {address.street}, {address.house_number}")
            # Проверка всех связанных адресов
            print("All addresses linked to buyer:", obj.addresses.all())

        # Добавление выбранных вручную адресов из формы
        if 'addresses' in form.cleaned_data:
            obj.addresses.add(*form.cleaned_data['addresses'])

        # Убедитесь, что все изменения сохранены
        obj.save()



admin.site.register(Buyer, BuyerAdmin)
admin.site.register(Address)
