from django.core.exceptions import ValidationError
from django.db import models

from buyers.models import Buyer
from products.models import Product


class Order(models.Model):
    objects = models.Manager()
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE,
                              related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_address = models.ForeignKey('buyers.Address', null=True,
                                         blank=True, on_delete=models.SET_NULL)

    def calculate_total_price(self):
        self.price = sum(item.product.price * item.quantity for item in
                         self.order_items.all())
        self.save()

    def to_dict(self):
        return {
            "order_id": self.id,
            "created_at": self.created_at,
            "price": str(self.price),
            "order_items": [
                {
                    "product_id": item.product.id,
                    "product_name": item.product.name,
                    "quantity": item.quantity
                }
                for item in self.order_items.all()
            ],
            "delivery_address": (
                str(self.delivery_address)
                if self.delivery_address
                else "Адрес доставки не указан"
            )
            #     self.delivery_address.street
            #     if self.delivery_address
            #     else "Адрес доставки не указан"
            # )
        }


class OrderItem(models.Model):
    objects = models.Manager()
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name="order_items")
    quantity = models.PositiveIntegerField(default=1)

    def clean(self):
        if self.quantity > self.product.count:
            raise ValidationError(
                f'Недостаточно товара: {self.product.name}. Доступно: {self.product.count}.')

    def save(self, *args, **kwargs):
        self.clean()  # Валидация перед сохранением
        self.product.count -= self.quantity  # Уменьшаем количество продукта
        self.product.save()  # Сохраняем изменения в продукте
        super().save(*args, **kwargs)  # Сохраняем OrderItem
