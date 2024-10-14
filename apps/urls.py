from django.urls import path, include

urlpatterns = [
    path('api/token/', .as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', .as_view(), name='token_refresh'),
    path('users/', include('users.urls')),
    path('shops', include('shops.urls'))
]
