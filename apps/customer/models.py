from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.db.models import F


class Profile(models.Model):
    """Customer profile for store user additionl information (like avatar, birthday, current balance...)."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text="Profile owner")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(), help_text="Current user balance")

    def update_balance(self, balance: Decimal) -> None:
        Profile.objects.select_for_update().filter(pk=self.pk).update(balance=F("balance") + balance)
