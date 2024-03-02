from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class UserProfile(models.Model):
    USER_ROLES = [
        ("creator", "Content Creator"),
        ("advertiser", "Advertiser"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=USER_ROLES)


class ContentCreator(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    # Ajoutez d'autres champs spécifiques au créateur de contenu


class Sponsor(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    # Ajoutez d'autres champs spécifiques au sponsor


# class Category(models.Model):
#     name = models.CharField(max_length=60)
#     slug = models.SlugField(blank=True)

#     @classmethod
#     def get_default_category(category):
#         default_category, _ = category.objects.get_or_create(name="Default", slug="_default")
#         return default_category

#     def __str__(self):
#         return self.name

#     def save(self, *args, **kwargs):
#         self.slug = self.slug or slugify(self.name)
#         super().save(*args, **kwargs)

# class User(models.Model):
#     name = models.CharField(max_length=128)
#     description = models.TextField(blank=True)
#     thumbnail = models.ImageField(upload_to="users_thumbnail", blank=True, null=True)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.description
