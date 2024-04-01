from django.db import models
from django.conf import settings
from django.forms import JSONField
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    USER_TYPE_CHOICES = (
        ("creator", "Creator"),
        ("advertiser", "Advertiser"),
        ("association", "Association"),
    )
    user_type = models.CharField(max_length=14, choices=USER_TYPE_CHOICES)



class CustomUserProfile(models.Model):

    name = models.CharField(max_length=255, unique=True, default="SOME STRING")
    social_links = models.JSONField(default=dict)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    main_description = models.TextField(
        verbose_name="Description",
        help_text="Enter a description for your model",
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
        default="static/images/profile_picture.jpg"
    )
