from django.db import models
from django.conf import settings
from django.db.models import JSONField
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):

    USER_TYPE_CHOICES = (
        ("creator", _("Créateur")),
        ("advertiser", _("Annonceur")),
        ("association", _("Association")),
    )
    user_type = models.CharField(max_length=14, choices=USER_TYPE_CHOICES)


class CustomUserProfile(models.Model):

    name = models.CharField(max_length=255, unique=True, default="SOME STRING")
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    short_description = models.TextField(
        verbose_name="Short description",
        help_text="Enter a short description",
        null=True,
        blank=True,
    )
    main_description = models.TextField(
        verbose_name="Description",
        help_text="Enter a description",
        null=True,
        blank=True,
    )
    second_description = models.TextField(
        verbose_name="Description",
        help_text="Enter a description",
        null=True,
        blank=True,
    )
    partners = models.JSONField(default=dict)
    banner = models.ImageField(
        upload_to="static/banners/",
        blank=True,
        null=True,
        default="static/images/default_banner.jpg",
    )
    profile_picture = models.ImageField(
        upload_to="static/profile_pictures/",
        blank=True,
        null=True,
        default="static/images/profile_picture.jpg",
    )
    instagram_url = models.URLField(
        max_length=255, null=True, blank=True, verbose_name="instagram"
    )
    x_url = models.URLField(max_length=255, null=True, blank=True, verbose_name="x")
    youtube_channel_url = models.URLField(
        max_length=255, null=True, blank=True, verbose_name="youtube"
    )
    twitch_url = models.URLField(
        max_length=255, null=True, blank=True, verbose_name="twitch"
    )
    tiktok_url = models.URLField(
        max_length=255, null=True, blank=True, verbose_name="tiktok"
    )
    snapchat_url = models.URLField(
        max_length=255, null=True, blank=True, verbose_name="snapchat"
    )
    contact_mail = models.EmailField(
        max_length=255, null=True, blank=True, verbose_name="Adresse e-mail"
    )
    services = JSONField(default=list, blank=True)

    def add_service(self, name, price):
        service = Service(name, str(price))  
        self.services.append(service.__dict__)
        self.save()

    def remove_service(self, index):
        del self.services[index]
        self.services = [service for service in self.services if isinstance(service['price'], str)]  
        self.save()


class Service:
    
    def __init__(self, name, price):
        self.name = name
        self.price = price
