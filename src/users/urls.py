# Django imports
from django.urls import path

from .views import *

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('update-access-token/', UpdateAccessTokenView.as_view(), name='update_access_token'),
    path('profile/', UserProfileView.as_view(), name='profile')
]
