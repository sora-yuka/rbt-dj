from django.db import models
from django.conf import settings
from apps.offers.models import OfferModel


class DealStatus(models.TextChoices):
    PROPOSED = "PROPOSED", "Proposed"
    ACCEPTED = "ACCEPTED", "Accepted"
    REJECTED = "REJECTED", "Rejected"
    CANCELLED = "CANCELLED", "Cancelled"


class OfferDealModel(models.Model):
    initiator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="initiated_deals",
    )
    responder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_deals",
    )
    initiator_offer = models.ForeignKey(
        OfferModel, on_delete=models.CASCADE, related_name="deals_as_initiator"
    )
    responder_offer = models.ForeignKey(
        OfferModel, on_delete=models.CASCADE, related_name="deals_as_responder"
    )
    status = models.CharField(
        max_length=20, choices=DealStatus.choices, default=DealStatus.PROPOSED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return (
            f"Deal {self.id}: {self.initiator.username} <-> {self.responder.username}"
        )
