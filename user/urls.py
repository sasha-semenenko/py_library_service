from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import CustomerCreateViewSet, ManageCustomerViewSet, CustomerViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)

app_name = "user"

urlpatterns = [
    path("create/", CustomerCreateViewSet.as_view(), name="create"),
    path("me/", ManageCustomerViewSet.as_view(), name="manage-customer"),

    # JWT token authentication
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
] + router.urls
