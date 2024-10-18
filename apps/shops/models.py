from django.db import models
from django.db.models import Model
from mptt.models import MPTTModel, TreeForeignKey

from apps.shared.models import TimeBasedModel
from shared.models import SlugBasedModel


class Section(TimeBasedModel):
    name_image = models.ImageField(upload_to='shops/categories/name_image/%Y/%m/%d', null=True, blank=True)
    intro = models.TextField(null=True, blank=True)
    banner = models.ImageField(upload_to='shops/categories/banner/%Y/%m/%d', null=True, blank=True)


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    section = models.ForeignKey('shops.Section', on_delete=models.CASCADE, null=True, blank=True,
                                related_name='categories')

    class MPTTMeta:
        order_insertion_by = ['name']





class Book(SlugBasedModel):
    title = models.CharField(max_length=255)
    author = models.ForeignKey('users.Author', on_delete=models.CASCADE, related_name='books')
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    pages = models.IntegerField()
    language = models.CharField(max_length=50)
    used_good_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    new_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ebook_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    audiobook_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.title




