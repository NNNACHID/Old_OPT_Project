# Generated by Django 5.0.2 on 2024-07-18 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0003_delete_campaignpayment_remove_campaign_max_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaigncollaboratorrequest',
            name='message',
            field=models.TextField(blank=True, null=True, verbose_name='Message'),
        ),
    ]
