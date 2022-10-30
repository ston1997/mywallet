from django.urls import path

from customer.views import UserBalanceAPIView


app_name = "customer"

api_url_patterns = [
    path("balance", UserBalanceAPIView.as_view(), name="balance"),
]

urlpatterns = api_url_patterns
