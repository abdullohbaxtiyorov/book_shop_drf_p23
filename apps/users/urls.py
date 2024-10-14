from .views import UserUpdateAPIView

from django.urls import path
from .views import UserRegistrationView, ActivateUserView, CustomTokenObtainPairView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateUserView.as_view(), name='activate'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('update/', UserUpdateAPIView.as_view(), name='user-update'),

]
