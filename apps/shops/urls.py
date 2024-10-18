from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# router.register(r'addresses', AddressModelViewSet, basename='address')

urlpatterns = [
    path('', include(router.urls)),
]