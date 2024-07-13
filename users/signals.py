from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import CustomUserProfile


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        CustomUserProfile.objects.create(
            user=instance, name=f"{instance.username}_profile"
        )


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    try:
        profile = instance.customuserprofile
    except CustomUserProfile.DoesNotExist:
        CustomUserProfile.objects.create(user=instance)
    else:
        profile.save()


@receiver(pre_save, sender=get_user_model())
def update_profile_name(sender, instance, **kwargs):
    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    if old_instance.username != instance.username:
        try:
            profile = instance.customuserprofile
            profile.name = f"{instance.username}_profile"
            profile.save()
        except CustomUserProfile.DoesNotExist:
            pass  
