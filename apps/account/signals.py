from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.account.models import Account
from apps.account.tasks import send_email


@receiver(post_save, sender=Account)
def send_email_user(sender, instance, created, **kwargs):
    if created:
        send_email.delay("Welcome to Our web site", "We are happy to see you here", [instance.email])