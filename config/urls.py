"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

from . import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

scheme_view = get_schema_view(
    info=openapi.Info(title="RBT", default_version="v1"),
    permission_classes=[permissions.AllowAny],
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("docs/", scheme_view.with_ui()),
    path("api/v1/users/", include("apps.users.urls")),
    path("api/v1/offers/", include("apps.offers.urls")),
    path("api/v1/deals/", include("apps.deals.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
