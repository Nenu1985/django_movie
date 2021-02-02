''' Here we setting up documentation rules using drf-yasg app'''

from django.conf import settings
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

if settings.DEBUG == True:
   url = 'http://127.0.0.1:8000/'
else:
   url = 'http://18.198.116.78'  # IP address of WEB server

schema_view = get_schema_view(
   openapi.Info(
      title="DRF Movie",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   url=url,
   public=True,
   permission_classes=(permissions.AllowAny,),  # documentations is allowed for everyone
)

urlpatterns = [
   path('swagger(<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]