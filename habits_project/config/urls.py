"""
URL configuration for habits_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers
from django.contrib import admin
from habits.views import HabitViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation for your habits app",
    ),
    public=True,
    # Remove the `renderer_classes` argument from here
)

router = routers.DefaultRouter()
router.register(r'habits', HabitViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('', include('docs.urls')),
    path('', include('users.urls')),
    path('admin/', admin.site.urls),
    path('api/documentation/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/documentation/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/documentation/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
