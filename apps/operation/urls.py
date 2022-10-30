from django.urls import path
from rest_framework.routers import SimpleRouter

from operation.views import OperationViewSet, TransactionAPIView, WithdrawalAPIView


app_name = "operation"
router = SimpleRouter()

router.register("", OperationViewSet, basename="operation")

api_url_patterns = [
    path("transaction", TransactionAPIView.as_view(), name="transaction"),
    path("withdrawal", WithdrawalAPIView.as_view(), name="withdrawal"),
]

urlpatterns = router.urls + api_url_patterns
