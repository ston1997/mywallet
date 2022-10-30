from rest_framework.response import Response
from rest_framework.views import APIView


class UserBalanceAPIView(APIView):
    """API view for return current user balance."""

    def get(self, request, *args, **kwargs) -> Response:
        return Response({"balance": request.user.profile.balance})
