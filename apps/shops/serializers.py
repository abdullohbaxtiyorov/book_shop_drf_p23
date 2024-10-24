from rest_framework.serializers import ModelSerializer

from apps.shops.models import Book


class BookModelSerializer(ModelSerializer):
    class Meta:
        model = Book
        extend = ()

