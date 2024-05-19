from django.db import models
import uuid

from app.bot.enums import LanguagesEnum


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=100)
    language = models.CharField(
        max_length=2,
        choices=LanguagesEnum.choices(),
        default=LanguagesEnum.IT.name
    )

    def __str__(self):
        return self.first_name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    link = models.URLField(max_length=200)
    last_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
