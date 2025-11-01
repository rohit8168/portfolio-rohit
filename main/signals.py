from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver

User = get_user_model()

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings

@receiver(post_migrate)
def create_super_user(sender, **kwargs):
    try:
        # Try fetching the user directly (avoids Djongo's bad SQL translation)
        User.objects.get(username=settings.SUPERUSER_USERNAME)
    except User.DoesNotExist:
        User.objects.create_superuser(
            username=settings.SUPERUSER_USERNAME,
            email=settings.SUPERUSER_EMAIL,
            password=settings.SUPERUSER_PASSWORD
        )
        print("✅ Superuser created automatically.")

