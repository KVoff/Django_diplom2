from django.db import models
from buyers.models import Buyer


class Profile(models.Model):
    # Связь с моделью Buyer через OneToOneField
    objects = models.Manager()
    buyer = models.OneToOneField(Buyer, on_delete=models.CASCADE,
                                 related_name="profile")
    bio = models.TextField()
    avatar_url = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.buyer.first_name} {self.buyer.last_name}"
