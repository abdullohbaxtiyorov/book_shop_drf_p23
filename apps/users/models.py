from django.contrib.auth.models import AbstractUser
from django.db.models import Model, ManyToManyField, EmailField, BooleanField

from users.managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = EmailField(unique=True)
    is_active = BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    wishlist = ManyToManyField('shops.Book', blank=True, related_name='wishlist')
