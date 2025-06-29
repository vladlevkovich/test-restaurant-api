from typing import Any, Type, cast

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Django REST Framework imports
from rest_framework import serializers, status
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .authentication import JWTAuthentication
from .models import User
from .serializers import (
    NewAccessTokenResponseSerializer,
    UpdateAccessTokenSerializer,
    UserEmailResponseSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
    UserRegisterSerializer,
    UserTokenResponseSerializer,
)


class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    @swagger_auto_schema(request_body=UserRegisterSerializer,
                         responses={
                             201: openapi.Response('Successful registration', UserEmailResponseSerializer())
                         })
    def post(self, request: Request, *args: Any, **kwargs: Any):
        return super().post(request, *args, **kwargs)

class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(request_body=UserLoginSerializer,
                         responses={
                             200: openapi.Response('Successful login', UserTokenResponseSerializer)
                         })
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        access_token = JWTAuthentication.create_access(user)
        refresh_token = JWTAuthentication.create_refresh(user)
        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token
        })

class UpdateAccessTokenView(GenericAPIView):
    serializer_class = UpdateAccessTokenSerializer

    @swagger_auto_schema(request_body=UpdateAccessTokenSerializer,
                         responses={
                             200: openapi.Response('Access token', NewAccessTokenResponseSerializer)
                         })
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.data['refresh_token']
        new_access_token = JWTAuthentication.update_access_token(refresh_token)
        return Response({'access_token': new_access_token}, status=status.HTTP_200_OK)

class UserProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self) -> Type[serializers.BaseSerializer]:
        if self.request.method == 'GET':
            return UserProfileSerializer
        return UserProfileUpdateSerializer

    def get_object(self) -> User:
        return cast(User, self.request.user)

    @swagger_auto_schema(
        responses={
            200: openapi.Response('User profile', UserProfileSerializer)
        }
    )
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=UserProfileUpdateSerializer,
        responses={
            200: openapi.Response('Updated profile', UserProfileSerializer)
        }
    )
    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().put(request, *args, **kwargs)
