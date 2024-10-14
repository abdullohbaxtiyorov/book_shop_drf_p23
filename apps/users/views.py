from drf_spectacular.utils import extend_schema
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import UpdateUserSerializer


@extend_schema(tags=['user'])
class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = IsAuthenticated,

    def get_object(self):
        return self.request.user

# @extend_schema(tags=['send'])
class CustomTokenObtainPairView(TokenObtainPairView):
    pass