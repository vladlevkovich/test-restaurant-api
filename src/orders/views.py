from typing import cast

# Django imports
from django.db.models import QuerySet

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Django REST Framework imports
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from src.users.models import User

from .models import Order
from .serializers import OrderCreateSerializer, OrderReadSerializer


class OrderListCreateView(GenericAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Creating a new order from items in the shopping cart",
        request_body=OrderCreateSerializer,
        responses={
            201: openapi.Response(
                description="Order created",
                schema=OrderReadSerializer()
            ),
            400: openapi.Response(description="Incorrect data or empty basket"),
            401: openapi.Response(description="Not authorized")
        }
    )
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(
            OrderReadSerializer(order).data,
            status=status.HTTP_201_CREATED
        )

class OrderDetailView(RetrieveAPIView[Order]):
    serializer_class = OrderReadSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Obtaining detailed information about the order",
        responses={
            200: openapi.Response(
                description="Detailed information about the orderня",
                schema=OrderReadSerializer()
            ),
            401: openapi.Response(description="Not authorized"),
            404: openapi.Response(description="Order not foundо")
        }
    )
    def get_queryset(self) -> QuerySet[Order]:
        user = cast(User, self.request.user)
        return Order.objects.filter(user=user)
