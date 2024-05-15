# Generated by Django 5.0.2 on 2024-04-03 14:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Campaigns', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='collaborater',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
