from django.urls import path, include

urlpatterns = [
    path('shops/', include('shops.urls')),
    path('users/', include('users.urls'))
]
