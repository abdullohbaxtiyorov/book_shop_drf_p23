from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.cache import cache
from django.utils.http import urlsafe_base64_decode
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status
from rest_framework.generics import UpdateAPIView, CreateAPIView, DestroyAPIView, ListCreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from users.email_service import ActivationEmailService
from users.models import User, Address
from users.serializers import UserUpdateSerializer, RegisterUserModelSerializer, LoginUserModelSerializer, \
    UserWishlist, AddressListModelSerializer


@extend_schema(tags=['user'])
class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = IsAuthenticated,

    def get_object(self):
        return self.request.user


@extend_schema(tags=['user'])
class UserWishlistCreateAPIViewDestroyAPIView(CreateAPIView, DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserWishlist
    permission_classes = IsAuthenticated,


@extend_schema(tags=['login-register'])
class RegisterCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserModelSerializer
    permission_classes = AllowAny,
    authentication_classes = ()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response = {
            'message': 'Successfully registered!'
        }
        activation_service = ActivationEmailService(user, request._current_scheme_host)
        activation_service.send_activation_email()
        return Response(response, status.HTTP_201_CREATED)


@extend_schema(tags=['login-register'])
class LoginAPIView(GenericAPIView):
    pass
#     serializer_class = LoginUserModelSerializer
#     permission_classes = [AllowAny]
#     authentication_classes = ()
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         email = serializer.validated_data['email']
#         password = serializer.validated_data['password']
#
#         user = authenticate(request=request, username=email, password=password)
#
#         if not user:
#             return self.handle_failed_login(request, email)
#
#         login_attempts_cache_key = f'failed_login_attempts_{user.id}'
#         blocked_cache_key = f'blocked_user_{user.id}'
#
#         if cache.get(blocked_cache_key):
#             return Response({'error': 'Siz 5 daqiqaga bloklandingiz.'}, status=status.HTTP_403_FORBIDDEN)
#
#         refresh = RefreshToken.for_user(user)
#
#         cache.delete(login_attempts_cache_key)
#
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         }, status=status.HTTP_200_OK)
#
#     def handle_failed_login(self, request, email):
#         login_attempts_cache_key = f'failed_login_attempts_{email}'
#         blocked_cache_key = f'blocked_user_{email}'
#
#         failed_attempts = cache.get(login_attempts_cache_key, 0)
#
#         failed_attempts += 1
#         cache.set(login_attempts_cache_key, failed_attempts, timeout=300)  # 5 daqiqa davomida saqlanadi
#
#         if failed_attempts >= 3:
#             cache.set(blocked_cache_key, True, timeout=300)  # 5 daqiqaga bloklash
#             return Response({'error': 'Siz 5 daqiqaga bloklandingiz.'}, status=status.HTTP_403_FORBIDDEN)
#
#     Response({'error': 'Email yoki parol noto‘g‘ri.'}, status=status.HTTP_401_UNAUTHORIZED)


@extend_schema(tags=['access-token'])
class ActivateUserView(APIView):
    authentication_classes = ()

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            uid, is_active = uid.split('/')
            user = User.objects.get(pk=uid, is_active=is_active)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and PasswordResetTokenGenerator().check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "User successfully verified!"})
        raise AuthenticationFailed('Havola yaroqsiz yoki muddati o‘tgan.')


@extend_schema(tags=['shops'])
class AddressListCreateAPIView(ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressListModelSerializer
    permission_classes = IsAuthenticated,

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


@extend_schema(tags=['shops'])
class AddressDestroyUpdateAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressListModelSerializer
    permission_classes = IsAuthenticated,

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user)
        self._can_delete = qs.count() > 1
        return qs

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if self._can_delete:
            _user: User = request.user
            if instance.id in (_user.billing_address_id, _user.shipping_address_id):
                return Response({"message": "maxsus addresslar"})

            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "ozi 1ta qoldi!"})
