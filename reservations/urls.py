from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
   openapi.Info(
      title="Room reservations API",
      default_version='v1',
      description='This API allows to managed employees, rooms and room reservations',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
]
