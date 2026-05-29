from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OfferViewSet, MyOffersListView

router = DefaultRouter()
router.register("", OfferViewSet, basename="offer")

urlpatterns = [
    path("me/", MyOffersListView.as_view(), name="my-offers-list"),
    path("", include(router.urls)),
]
