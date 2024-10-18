from django.core.management.base import BaseCommand
from faker import Faker

from users.models import User


class Command(BaseCommand):
    model_list = {'user'}

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        self.f = Faker()
        super().__init__(stdout, stderr, no_color, force_color)

    def add_arguments(self, parser):
        for model in self.model_list:
            parser.add_argument(f'--{model}', type=int, default=0)

    def _user(self, count=0):
        user_list = list()
        for _ in range(count):
            user_list.append(User(
                email=self.f.email(domain='gmail.com'),
                first_name=self.f.first_name(),
                last_name=self.f.last_name(),
                is_active=self.f.boolean(),
                password=self.f.password(),
                last_login=self.f.date_time()
            )
            )
        User.objects.bulk_create(user_list)
        self.stdout.write(self.style.SUCCESS(F"User malumotlari f{count} tadan qoshildi"))

    def handle(self, *args, **options):
        for name in self.model_list & set(options):
            getattr(self, f'_{name}')(options[name])

        self.stdout.write(self.style.SUCCESS(f"Barcha malumotlar qo'shild"))

