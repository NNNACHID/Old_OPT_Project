from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from users.models import CustomUser
from campaigns.models import Campaign


class Transaction(models.Model):
    amount = models.DecimalField(
        ("Amount"),
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    sender = models.ForeignKey(
        CustomUser, related_name="sent_transactions", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        CustomUser, related_name="received_transactions", on_delete=models.CASCADE
    )
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True
        ordering = ['-date']

    def __str__(self):
        return (
            f"Transaction from {self.sender} to {self.receiver} - Amount: {self.amount}"
        )


class CampaignTransaction(Transaction):
    campaign = models.ForeignKey(
        Campaign, related_name="transactions", on_delete=models.CASCADE
    )
