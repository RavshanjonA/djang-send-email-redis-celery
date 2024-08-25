# Send Email with Celery, Redis in Django

#### This is a simple example of how to send email with celery and django.

## Setup

1. ```pip install celery redis```
2. Add these codes to ```settings.py```
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'sender@email.com'
EMAIL_HOST_PASSWORD = 'get pass [link](https://myaccount.google.com/apppasswords) '
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
```

3. Create ```celery.py``` in the config folder:
```python
import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('celery')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = 'redis://localhost:6379/0'

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

```


4. Create ```tasks.py``` in the app folder:

```python
import os

from django.core.mail import send_mail

from config.celery import app


@app.task
def send_email(subject, message, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email=os.getenv("SENDER_EMAIL"),
        recipient_list=recipient_list
    )
```
5. Example Usage
You can now use the send_email task in your Django views or models to send emails asynchronously. For example:
```python
from apps.account.tasks import send_email

send_email.delay('Subject', 'Message', ['recipient@example.com'])
```
6. Run celery worker
```python
celery -A config worker -l INFO
```
