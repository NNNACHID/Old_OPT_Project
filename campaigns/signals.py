from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *




# @receiver(post_save, sender=CampaignPartnerRequest)
# def send_partner_request_notification(sender, instance, created, **kwargs):
#     if created:
#         partner = instance.partner
#         campaign = instance.campaign
        
#         # send_mail(
            
#         # )
        
#         Notification.objects.create(
#             user=partner,
#             message=f"Vous avez une nouvelle demande de partnariat émise par {campaign.campaign_creator} !"
#         )