from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField()

class Users(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="users", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
