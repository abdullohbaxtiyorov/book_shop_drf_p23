from django.contrib import admin
from django.urls import include,path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# urls.py

urlpatterns = [

    path('api/v1/', include('apps.urls')),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api-auth/', include('rest_framework.urls'))
]
