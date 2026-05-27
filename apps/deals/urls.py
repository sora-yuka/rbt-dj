from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OfferDealViewSet, PublicPlatformAnalyticsView, PrivateUserAnalyticsView

router = DefaultRouter()
router.register("", OfferDealViewSet, basename="deal")

urlpatterns = [
    path("analytics/global/", PublicPlatformAnalyticsView.as_view(), name="global-analytics"),
    path("analytics/me/", PrivateUserAnalyticsView.as_view(), name="private-analytics"),
    path("", include(router.urls)),
]
