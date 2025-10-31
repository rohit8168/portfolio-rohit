from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver

User = get_user_model()

@receiver(post_migrate)
def create_super_user(sender, **kwargs):
    if not User.objects.filter(username=settings.SUPERUSER_USERNAME).exists():
        User.objects.create_superuser(
            username=settings.SUPERUSER_USERNAME,
            email=settings.SUPERUSER_EMAIL,
            password=settings.SUPERUSER_PASSWORD
        )
        print("Superuser created automatically")
