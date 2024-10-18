from celery import shared_task
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import timezone

from root.settings import EMAIL_HOST_USER
from .models import User


@shared_task
def delete_inactive_users_task():
    now = timezone.now()
    inactive_users = User.objects.filter(is_active=False, activation_deadline__lt=now)
    deleted_count, _ = inactive_users.delete()
    print(f"{deleted_count} foydalanuvchi o'chirildi.")


@shared_task
def delete_cache_task(cache_key):
    cache.delete(cache_key)
    print(f"Cache key {cache_key} successfully deleted.")
    return f"Cache key {cache_key} successfully deleted."


@shared_task
def send_activation_email_task(subject, message, recipient_list, html_message):
    for recipient in recipient_list:
        cache_key = f'activation_email:{recipient}'
        cache.set(cache_key, message, timeout=60)
        cached_message = cache.get(cache_key)
        print(f"Cache set for {recipient}: {cached_message}")
        send_mail(subject, message, EMAIL_HOST_USER, [recipient], html_message=html_message)
        print(f"Email sent to {recipient}.")
        delete_cache_task.apply_async((cache_key,), countdown=60)
    return f"Emails sent to {', '.join(recipient_list)} and cache keys created."
