from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField("Название", max_length=255)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    image_url = models.URLField("Ссылка на фото", blank=True, null=True)
    description = models.TextField("Полное описание", blank=True, null=True)  # <-- новое поле

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total(self):
        return self.product.price * self.quantity