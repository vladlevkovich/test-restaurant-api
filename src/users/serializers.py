from typing import Any, Dict, List, TypedDict

# Django REST Framework imports
from rest_framework import serializers

from src.orders.serializers import OrderReadSerializer

from .models import User


class _UserRegisterData(TypedDict):
    email: str
    password: str
    password_check: str

class _UserLoginData(TypedDict):
    email: str
    password: str
    user: User

class UserEmailResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)

class UserTokenResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()

class UpdateAccessTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

class NewAccessTokenResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()

class UserRegisterSerializer(serializers.ModelSerializer[User]):
    password = serializers.CharField(write_only=True, min_length=8)
    password_check = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_check')

    def validate(self, attrs: Dict[str, Any]) -> _UserRegisterData:
        if attrs['password'] != attrs['password_check']:
            raise serializers.ValidationError('Passwords do not match.')
        return attrs    # type: ignore[return-value]

    def create(self, validated_data: _UserRegisterData) -> User:
        email = validated_data.get('email')
        if email is None:
            raise serializers.ValidationError('Email is required.')
        user = User.objects.create(email=email)
        user.set_password(validated_data.get('password'))
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    def validate(self, attrs: Dict[str, Any]) -> _UserLoginData:
        email = attrs['email']
        password = attrs['password']
        user = User.objects.filter(email=email).first()
        if not user or not user.check_password(password):
            raise serializers.ValidationError('Incorrect email or password.')
        attrs['user'] = user
        return attrs    # type: ignore[return-value]

class UserProfileSerializer(serializers.ModelSerializer):
    orders = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'orders')

    def get_orders(self, obj: User) -> Dict[str, Any]:
        orders = obj.orders.all().order_by('-created_at')
        return OrderReadSerializer(orders, many=True).data

class UserProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')

