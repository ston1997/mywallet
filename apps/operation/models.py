import uuid

from django.contrib.auth.models import User
from django.db import models


class Operation(models.Model):
    """
    Model for store any user financial operations.
    """

    class Type(models.TextChoices):
        """
        Choice model for different operation types.
        """

        PURCHASE = "PURCHASE", "Transaction:Purchase"  # positive
        REFUND = "REFUND", "Transaction:Refund"  # negative
        WITHDRAWAL = "WITHDRAWAL", "Withdrawal"  # negative

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Main operation identification")
    transaction_id = models.IntegerField(null=True)
    created = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2, help_text="Balance after current transaction")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kind = models.CharField(max_length=10, choices=Type.choices)
