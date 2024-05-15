from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from Users.models import CustomUser


class Campaign(models.Model):
    name = models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text=_(""),
    )
    campaign_creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_campaigns')
    collaborators = models.ManyToManyField(
        CustomUser, related_name="campaigns_participated"
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
    
    def accept(self):
        self.accepted = True
        self.save()

    def decline(self):
        self.campaign.remove_collaborator(self.collaborator)
        self.delete()
