from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import CustomUserProfile


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        CustomUserProfile.objects.create(
            user=instance, name=f"{instance.username}_profile"
        )
        print("oi")


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    try:
        profile = instance.customuserprofile
    except CustomUserProfile.DoesNotExist:
        CustomUserProfile.objects.create(user=instance)
    else:
        profile.save()
