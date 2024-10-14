from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from rest_framework.fields import EmailField, CharField
from rest_framework.serializers import ModelSerializer, Serializer

from users.models import User


class UpdateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class EmailModelSerializer(Serializer):
    email = EmailField(help_text='Enter email')


class VerifyModelSerializer(Serializer):
    email = EmailField(help_text='Enter email')
    code = CharField(max_length=8, help_text='Enter confirmation code')

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        cache_code = str(cache.get(email))

        if code != cache_code:
            raise ValidationError({'code': 'Code not found or timed out'})

        return attrs
