from rest_framework.generics import ListAPIView

from apps.shops.models import Book
from apps.shops.serializers import BookModelSerializer


class BookListview(ListAPIView):
    queryset = Book.objects.all
    serializer_class = BookModelSerializer






