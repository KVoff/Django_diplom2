from django.db import models


class Product(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    class Meta:
        permissions = [
            ("can_view_product", "Can view product"),
            ("can_add_product", "Can add product"),
            ("can_change_product", "Can change product"),
            ("can_delete_product", "Can delete product"),
        ]

    def __str__(self):
        return f"{self.name} - {self.price}"

    def to_dict(self):
        return {
            "id": self.pk,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "count": self.count,
            "image_url": self.image.url if self.image else None,
        }

    # # проверка и обновление товара для магазина
    # def reduce_stock(self, quantity):
    #     if quantity > self.count:
    #         return False
    #     self.count -= quantity
    #     self.save()
    #     return True
