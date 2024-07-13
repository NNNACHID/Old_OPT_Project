from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import *


@receiver(m2m_changed, sender=Campaign.collaborators.through)
def create_campaign_collaborator_requests(sender, instance, action, **kwargs):
    if action == 'post_add':
        for collaborator in instance.collaborators.all():
            CampaignCollaboratorRequest.objects.create(
                campaign=instance, collaborator=collaborator
            )
