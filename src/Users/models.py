from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField()
    
    @classmethod
    def get_default_category(category):
        category.objects.get_or_create(name="Default", slug="default")

class User(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="users_thumbnail", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
