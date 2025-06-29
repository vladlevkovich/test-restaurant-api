from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Django REST Framework imports
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Dish
from .serializers import DishSerializer


class DishListView(GenericAPIView[Dish]):
    serializer_class = DishSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Obtaining a list of available dishes",
        operation_summary="Dishes list",
        responses={
            200: openapi.Response(
                description="List of available dishes",
                schema=DishSerializer(many=True)
            ),
            401: openapi.Response(description="Not authorized")
        }
    )
    def get(self, request: Request) -> Response:
        dishes = Dish.objects.filter(is_available=True)
        serializer = self.serializer_class(dishes, many=True)
        return Response(serializer.data)
