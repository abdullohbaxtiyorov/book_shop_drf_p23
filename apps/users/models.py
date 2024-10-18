from django.contrib.auth.models import AbstractUser
from django.db.models import Model, ManyToManyField, EmailField, BooleanField, ForeignKey, CASCADE, \
    CharField, TextField, OneToOneField, RESTRICT, PositiveIntegerField

from shared.models import SlugBasedModel, TimeBasedModel
from users.managers import CustomUserManager


class Wishlist(TimeBasedModel):
    user = ForeignKey('users.User', on_delete=CASCADE, related_name='wishlists')  # O'zgartirildi
    book = ForeignKey('shops.Book', on_delete=CASCADE, related_name='wishlists')


class Cart(TimeBasedModel):
    book = ForeignKey('shops.Book', CASCADE)
    owner = ForeignKey('users.User', CASCADE)
    quantity = PositiveIntegerField(db_default=1)
    '''
    format
    condition
    seller
    ship from
    '''

    def __str__(self):
        return f"{self.owner} - {self.book}"


class Country(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = None
    email = EmailField(unique=True)
    is_active = BooleanField(default=False)
    shipping_address = OneToOneField('users.Address', RESTRICT, null=True, blank=True, related_name='shipping_user')
    billing_address = OneToOneField('users.Address', RESTRICT, null=True, blank=True, related_name='billing_user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    wishlist = ManyToManyField('shops.Book', blank=True, related_name='wishlist')


class Address(Model):
    user = ForeignKey('users.User', CASCADE)
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255, blank=True, null=True)
    country = CharField(max_length=100)
    address_line_1 = CharField(max_length=255)
    address_line_2 = CharField(max_length=255, blank=True, null=True)
    city = ForeignKey('Country', CASCADE)
    state_province = CharField(max_length=100)
    postal_code = CharField(max_length=20)
    phone_number = CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"


class Author(Model):
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    description = TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name}{self.last_name}"
