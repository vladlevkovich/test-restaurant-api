# Django imports
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# Django REST Framework imports
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Restaurant API",
      default_version='v1',
      description="Документація API ресторану",
      contact=openapi.Contact(email="your@email.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('src.users.urls')),
    path('cart/', include('src.cart.urls')),
    path('orders/', include('src.orders.urls')),
    path('menu/', include('src.menu.urls')),

    # Swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
