from django.contrib import admin
from django.contrib.admin import ModelAdmin
from mptt.admin import DraggableMPTTAdmin

from shops.models import Book, Category


@admin.register(Category)
class Category(DraggableMPTTAdmin):
    pass

@admin.register(Book)
class BookModelAdmin(ModelAdmin):
    pass