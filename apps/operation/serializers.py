from datetime import datetime
from typing import Dict

from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers

from operation.utils import create_operation_and_update_balance
from operation.models import Operation


class OperationListSerializer(serializers.ModelSerializer):
    """Serializer for represent list of users operations."""

    kind = serializers.SerializerMethodField()

    class Meta:
        model = Operation
        fields = (
            "uid",
            "transaction_id",
            "created",
            "amount",
            "balance",
            "kind"
        )

    @staticmethod
    def get_kind(obj: Operation) -> str:
        return obj.get_kind_display()


class TransactionSerializer(serializers.ModelSerializer):
    """Class for serialize and validate transaction data and create operation."""

    user_id = serializers.IntegerField()
    transaction_id = serializers.IntegerField()
    created = serializers.DateTimeField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Operation
        fields = ("transaction_id", "user_id", "created", "amount")

    def validate_user_id(self, value: int) -> int:
        if not User.objects.filter(id=value).exists():
            raise ValueError({"user_id": ["User doesn't exist in system"]})

        return value

    def create(self, validated_data: Dict) -> Operation:
        user = User.objects.get(id=validated_data["user_id"])

        # Define what type of transaction we got
        if validated_data["amount"] > 0:
            kind = Operation.Type.PURCHASE
        else:
            kind = Operation.Type.REFUND

        operation = Operation.objects.filter(transaction_id=validated_data["transaction_id"]).last()
        # In more real case some 3-rd party system send same request (with same data) to check transaction status
        # off course its could be some  3-rd party system problems - we don't have to process the operation
        if operation:
            return operation

        with transaction.atomic():
            balance_after_transaction = user.profile.balance + validated_data["amount"]
            operation = create_operation_and_update_balance(
                {
                    "amount": validated_data["amount"],
                    "created": validated_data["created"],
                    "transaction_id": validated_data["transaction_id"],
                    "user": user,
                    "kind": kind,
                    "balance": balance_after_transaction
                }
            )

        return operation


class WithdrawalSerializer(serializers.ModelSerializer):
    """Class for serialize and validate withdrawal data and create operation."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Operation
        fields = ("amount", "user")

    def create(self, validated_data: Dict) -> Operation:
        user = validated_data["user"]
        kind = Operation.Type.WITHDRAWAL
        amount = abs(validated_data["amount"])

        with transaction.atomic():
            balance_after_withdrawal = user.profile.balance - amount
            operation = create_operation_and_update_balance(
                {
                    "amount": -amount,
                    "created": datetime.utcnow(),
                    "user": user,
                    "kind": kind,
                    "balance": balance_after_withdrawal
                }
            )

        return operation
