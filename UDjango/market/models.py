from django.db import models
from django.core.exceptions import ValidationError
from buyers.models import Buyer
from products.models import Product


class Cart(models.Model):
    buyer = models.OneToOneField(Buyer, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='CartItem')

    def get_total_price(self):
        return sum(item.product.price * item.quantity for item in
                   self.cart_items.all())

    def get_position_price(self):
        return (item.product.price * item.quantity for item in
                   self.cart_items.all())

    # Возвращаем все CartItem для данной корзины
    @property
    def cart_items(self):
        return self.cartitem_set.all()



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def clean(self):
        if self.quantity > self.product.count:
            raise ValidationError(f"Недостаточно товара: {self.product.name}.")
