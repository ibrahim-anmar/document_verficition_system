from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

urlpatterns = [
    path('api_schema',get_schema_view(title='API Schema', description='API for document verification'), name='api_schema'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='docs.html', 
        extra_context={'schema_url':'api_schema'}
        ), name='swagger-ui'),
    path('admin/', admin.site.urls),
    path('', include('imgapp.urls')),
]
