from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser


class Campaign(models.Model):
    name = models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    # min_price = models.IntegerField(
    #     default=60
    # )
    # max_price = models.IntegerField(
    #     default=5000
    # )
    is_open = (
        models.BooleanField(
            default=True,
        ),
    )
    campaign_creator = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="created_campaigns"
    )
    collaborators = models.ManyToManyField(
        CustomUser, related_name="campaigns_participated"
    )
    partner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="campaign_partner",
        limit_choices_to={"user_type": "creator"},
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _("Campaign")
        verbose_name_plural = _("Campaigns")
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gte=models.F("start_date")),
                name="end_date_must_be_after_start_date",
            )
        ]

    def __str__(self):
        return self.name

    def add_collaborator(self, collaborator):
        self.collaborators.add(collaborator)

    def remove_collaborator(self, collaborator):
        self.collaborators.remove(collaborator)


class CampaignCollaboratorRequest(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    collaborator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    message = models.TextField(verbose_name=_("Message"), null=True, blank=True)

    def accept(self):
        self.accepted = True
        self.campaign.add_collaborator(self.collaborator)
        self.save()
        self.delete()

    def decline(self):
        self.delete()
