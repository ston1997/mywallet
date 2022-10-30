from typing import Dict

from operation.models import Operation


def create_operation_and_update_balance(operation_data: Dict) -> Operation:
    """Method for create financial operation and update customer current balance."""
    user = operation_data["user"]
    amount = operation_data["amount"]

    # Create financial operation
    financial_operation = Operation.objects.create(**operation_data)

    # Update current user balance
    user.profile.update_balance(amount)

    return financial_operation
