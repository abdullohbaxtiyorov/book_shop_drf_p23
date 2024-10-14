from django.urls import path
from .views import UserUpdateAPIView
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import CustomTokenObtainPairView
urlpatterns = [

    path('login', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token', TokenRefreshView.as_view(), name='token_refresh'),

    path('update/', UserUpdateAPIView.as_view(), name='user-update'),
]
# urlpatterns = [
# ]
