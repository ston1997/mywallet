from rest_framework.generics import CreateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from django.db.models import QuerySet

from operation.serializers import OperationListSerializer, TransactionSerializer, WithdrawalSerializer
from operation.models import Operation


class OperationViewSet(GenericViewSet, ListModelMixin):
    """API ViewSet for return list of user financial operations with pagination."""

    serializer_class = OperationListSerializer

    def get_queryset(self) -> QuerySet[Operation]:
        """Overwritten method for get QuerySet of Operation objects, filtered by owner and ordered DESC by created."""

        return Operation.objects.filter(user=self.request.user).order_by("-created")


class TransactionAPIView(CreateAPIView):
    """API view for process transaction request from 3-rd party systems."""

    permission_classes = (AllowAny,)
    serializer_class = TransactionSerializer


class WithdrawalAPIView(CreateAPIView):
    """API view for process user withdrawal operations."""

    serializer_class = WithdrawalSerializer
