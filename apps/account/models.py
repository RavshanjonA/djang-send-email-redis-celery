from django.contrib.auth.models import AbstractUser
from django.db.models import EmailField


class Account(AbstractUser):
    email = EmailField(unique=True, )
