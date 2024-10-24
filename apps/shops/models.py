from django.db.models import ImageField, CharField, ForeignKey, CASCADE, TextField, DecimalField
from django.utils.text import slugify
from django_jsonform.models.fields import JSONField
from mptt.models import MPTTModel, TreeForeignKey

from apps.shared.models import TimeBasedModel, SlugBasedModel


class Section(TimeBasedModel):
    name_image = ImageField(upload_to='shops/categories/name_image/%Y/%m/%d', null=True, blank=True)
    intro = TextField(null=True, blank=True)
    banner = ImageField(upload_to='shops/categories/banner/%Y/%m/%d', null=True, blank=True)


class Category(MPTTModel):
    name = CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=CASCADE, null=True, blank=True, related_name='subcategories')
    section = ForeignKey('Section', on_delete=CASCADE, null=True, blank=True,
                         related_name='categories')

    class MPTTMeta:
        order_insertion_by = ['name']


class Book(SlugBasedModel):
    SCHEMA = {
        'type': 'dict',  # or 'object'
        'keys': {  # or 'properties'
            'format': {
                'type': 'string',
                'title': 'Format'
            },
            'publisher': {
                'type': 'string',
                'title': 'Publisher',
            },
            'pages': {
                'type': 'integer',
                'title': 'Pages',
                'helpText': '(Optional)'
            },
            'dimensions': {
                'type': 'string',
                'title': 'Dimensions',
                'helpText': 'exp. 6.30 x 9.20 x 1.20 inches'
            },
            'shipping_weight': {
                'type': 'number',
                'title': 'Shipping Weight',
                'helpText': 'lbs'
            },
            'languages': {
                'type': 'string',
                'title': 'Language'
            },
            'publication_date': {
                'type': 'string',
                'title': 'Publication Date'
            },
            'isbn_13': {
                'type': 'integer',
                'title': 'ISBN-13'
            },
            'isbn_10': {
                'type': 'integer',
                'title': 'ISBN-10'
            },
            'edition': {
                'type': 'integer',
                'title': 'Edition',
                'helpText': '(Optional)'
            },
        },
        'required': ['format', 'languages', 'isbn_13', 'isbn_10', 'shipping_weight', 'dimensions', 'publication_date']
    }
    title = CharField(max_length=255)
    used_good_price = DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    new_price = DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ebook_price = DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    audiobook_price = DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    image = ImageField(upload_to='shops/books/%Y/%m/%d', null=True, blank=True)
    category = ForeignKey('Category', CASCADE)

    features = JSONField(schema=SCHEMA)

    def save(self, *args, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = f"{slugify(self.title)}-{self.features['isbn_13']}"

        super().save(*args, force_insert=force_insert, force_update=force_update, using=using,
                     update_fields=update_fields)
