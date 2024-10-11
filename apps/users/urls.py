from django.urls import path
from .views import UserUpdateAPIView

urlpatterns = [
    path('update/', UserUpdateAPIView.as_view(), name='user-update'),
]
# urlpatterns = [
# ]
