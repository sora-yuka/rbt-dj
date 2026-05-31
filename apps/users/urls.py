from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterAPIView, CustomTokenObtainPairView

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="user_register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh_pair")
]
