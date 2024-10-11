from django.db.models import CharField, CASCADE, TextField, ImageField, Model, ForeignKey, DateField, IntegerField, \
    DecimalField
from mptt.models import MPTTModel, TreeForeignKey

from apps.shared.models import TimeBasedModel
from shared.models import SlugBasedModel


class Section(TimeBasedModel):
    name_image = ImageField(upload_to='shops/categories/name_image/%Y/%m/%d', null=True, blank=True)
    intro = TextField(null=True, blank=True)
    banner = ImageField(upload_to='shops/categories/banner/%Y/%m/%d', null=True, blank=True)


class Category(MPTTModel):
    name = CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', CASCADE, null=True, blank=True, related_name='subcategories')
    section = ForeignKey('shops.Section', CASCADE, null=True, blank=True, related_name='categories')

    class MPTTMeta:
        order_insertion_by = ['name']

class Book(SlugBasedModel):
    title = CharField(max_length=255)
    author = ForeignKey('shops.Author', CASCADE, related_name=' books' )
    isbn = CharField(max_length=13, unique=True)
    publication_date = DateField()
    pages = IntegerField()
    price = DecimalField(max_digits=6, decimal_places=2)
    language = CharField(max_length=50)

    def __str__(self):
        return self.title

class Author(SlugBasedModel):
    name = CharField(max_length=50)
    def __str__(self):
        return self.name
