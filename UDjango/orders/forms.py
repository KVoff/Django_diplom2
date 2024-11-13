from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from buyers.models import Buyer, Address
from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    buyer = forms.ModelChoiceField(queryset=Buyer.objects.all(), required=True,
                                   label="Buyer")

    class Meta:
        model = Order
        fields = ['buyer']

    def save(self, commit=True):
        order = super().save(commit=False)

        if commit:
            order.save()  # Сохраняем заказ
        return order


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    def clean_quantity(self):
        product = self.cleaned_data.get('product')
        quantity = self.cleaned_data.get('quantity')

        if product and quantity:
            if quantity > product.count:
                raise ValidationError(
                    _("Недостаточно товара: %(product_name)s. Доступно: %(available)d."),
                    params={'product_name': product.name,
                            'available': product.count},
                )
        return quantity


class OrderUpdateForm(forms.ModelForm):
    new_street = forms.CharField(required=False, max_length=255,
                                 label="New Street")
    new_house_number = forms.CharField(required=False, max_length=10,
                                       label="New House Number")

    class Meta:
        model = Order
        fields = ['delivery_address']

    def save(self, commit=True):
        order = super().save(commit=False)

        new_street = self.cleaned_data.get('new_street')
        new_house_number = self.cleaned_data.get('new_house_number')

        if new_street and new_house_number:
            # Проверяем, существует ли уже такой адрес
            address, created = Address.objects.get_or_create(street=new_street,
                                                             house_number=new_house_number)
            # Обновляем адрес доставки
            order.delivery_address = address

        if commit:
            order.save()
        return order
