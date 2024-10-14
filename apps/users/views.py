from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import UpdateUserSerializer, UserRegistrationSerializer
from .email_service import ActivationEmailService
from .models import User
from .serializers import CustomTokenObtainPairSerializer


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


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        # Tasdiqlash emailini yuborish
        activation_service = ActivationEmailService(user)
        activation_service.send_activation_email()


class ActivateUserView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and PasswordResetTokenGenerator().check_token(user, token):
            user.is_active = True
            user.save()

            # JWT token yaratish
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),  # Refresh tokenini qaytarish
                'access': str(refresh.access_token),  # Access tokenini qaytarish
            })
        raise AuthenticationFailed('Havola yaroqsiz yoki muddati o‘tgan.')



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
