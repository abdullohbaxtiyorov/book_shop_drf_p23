from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, BooleanField, Model, ForeignKey, ManyToManyField, CASCADE


class User(AbstractUser):
    wishlist = ManyToManyField('shops.Book', blank=True, related_name='wishlist')


class AddressBookEntry(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255, blank=True, null=True)
    country = CharField(max_length=100)
    address_line_1 = CharField(max_length=255)
    address_line_2 = CharField(max_length=255, blank=True, null=True)
    city = CharField(max_length=100)
    state_province = CharField(max_length=100)
    postal_code = CharField(max_length=20)
    phone_number = CharField(max_length=20)
    is_default_shipping = BooleanField(default=False)
    is_default_billing = BooleanField(default=False)


class ReviewBookEntry(Model):
    user = ForeignKey('users.User', CASCADE)
    description = CharField(max_length=255)
