from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    USER_TYPE_CHOICES = (
        ("creator", "Creator"),
        ("advertiser", "Advertiser"),
        ("association", "Association"),
    )
    user_type = models.CharField(max_length=14, choices=USER_TYPE_CHOICES)
    description = models.TextField(
        verbose_name="Description",
        help_text="Enter a description for your model",
        null=True,
        blank=True,
    )

    def is_creator(self):
        return self.user_type == "creator"

    def is_advertiser(self):
        return self.user_type == "advertiser"

    def is_association(self):
        return self.user_type == "association"