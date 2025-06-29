from typing import Any, Type, cast
import uuid

# Django imports
from django.db.models import QuerySet

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Django REST Framework imports
from rest_framework import generics, serializers, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from src.users.models import User

from .models import Cart, CartItem
from .serializers import CartItemReadSerializer, CartItemWriteSerializer, CartSerializer


class CartItemListCreateView(ListCreateAPIView[CartItem]):
    """
        Отримання всіх товарів у кошику або додавання нового товару.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[CartItem]:
        user = cast(User, self.request.user)
        return CartItem.objects.filter(cart__user=user).select_related('dish')

    def get_serializer_class(self) -> Type[serializers.BaseSerializer]:
        return CartItemReadSerializer if self.request.method == 'GET' else CartItemWriteSerializer

    @swagger_auto_schema(
        operation_description="Obtaining a list of items in the shopping cart with the total amount",
        responses={
            200: openapi.Response(
                description="List of goods and total amount",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'items': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=CartItemReadSerializer()
                        ),
                        'total': openapi.Schema(type=openapi.TYPE_NUMBER)
                    }
                )
            ),
            401: openapi.Response(description="Not authorized")
        }
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        queryset = self.get_queryset()
        serializer = CartItemReadSerializer(queryset, many=True,
                                            context=self.get_serializer_context())

        total = sum(item.dish.price * item.quantity for item in queryset)

        return Response(
            {
                "items": serializer.data,
                "total": total
            },
            status=status.HTTP_200_OK
        )

    def perform_create(self, serializer: serializers.BaseSerializer[CartItem]) -> None:
        user = cast(User, self.request.user)
        cart, _ = Cart.objects.get_or_create(user=user)
        write_serializer = cast(CartItemWriteSerializer, serializer)
        item, created = CartItem.objects.get_or_create(cart=cart, dish=write_serializer.validated_data['dish'])
        quantity = write_serializer.validated_data['quantity']
        item.quantity = item.quantity + quantity if not created else quantity
        item.save()

class CartItemDetailView(RetrieveUpdateDestroyAPIView[CartItem]):
    """
        Перегляд, оновлення або видалення конкретної позиції в кошику.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemWriteSerializer

    def get_queryset(self) -> QuerySet[CartItem]:
        user = cast(User, self.request.user)
        return CartItem.objects.filter(
            cart__user=user).select_related('dish')

    @swagger_auto_schema(
        operation_description="Updating the quantity of items in the shopping cart",
        request_body=CartItemWriteSerializer,
        responses={
            200: openapi.Response(
                description="Product updated",
                schema=CartItemReadSerializer()
            ),
            400: openapi.Response(description="Invalid data"),
            401: openapi.Response(description="Not authorized"),
            404: openapi.Response(description="Product not found")
        },
    )
    def put(self, request: Request, pk: uuid.UUID, *args: Any, **kwargs: Any) -> Response:
        item = generics.get_object_or_404(self.get_queryset(), pk=pk)
        serializer  = self.serializer_class(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            CartItemReadSerializer(item, context=self.get_serializer_context()).data,
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_description="Removing items from the shopping cart",
        responses={
            204: openapi.Response(description="Product removed"),
            401: openapi.Response(description="Not authorized"),
            404: openapi.Response(description="Product not found")
        }
    )
    def delete(self, request: Request, pk: uuid.UUID, *args: Any, **kwargs: Any) -> Response:
        item = generics.get_object_or_404(self.get_queryset(), pk=pk)
        item.delete()
        return Response({'message': 'Item removed'}, status=status.HTTP_204_NO_CONTENT)
