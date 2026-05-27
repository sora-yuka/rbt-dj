from django.db.models import Q
from rest_framework import serializers

from apps.offers.serializers import OfferReadSerializer
from .models import OfferDealModel, DealStatus, OfferModel


class DealReadSerializer(serializers.ModelSerializer):
    initiator = serializers.ReadOnlyField(source="initiator.username")
    responder = serializers.ReadOnlyField(source="responder.username")
    initiator_offer = OfferReadSerializer(read_only=True)
    responder_offer = OfferReadSerializer(read_only=True)

    class Meta:
        model = OfferDealModel
        fields = [
            "id",
            "initiator",
            "responder",
            "initiator_offer",
            "responder_offer",
            "status",
            "created_at",
            "completed_at",
        ]

    def to_representation(self, instance) -> dict:
        representation = super().to_representation(instance)
        if instance.created_at:
            representation["created_at"] = instance.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        if instance.completed_at:
            representation["completed_at"] = instance.completed_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        return representation


class DealWriteSerializer(serializers.ModelSerializer):
    initiator_offer = serializers.PrimaryKeyRelatedField(
        queryset=OfferModel.objects.all()
    )
    responder_offer = serializers.PrimaryKeyRelatedField(
        queryset=OfferModel.objects.all()
    )

    class Meta:
        model = OfferDealModel
        fields = ["initiator_offer", "responder_offer"]

    def validate(self, data: dict) -> dict:
        init_offer = data["initiator_offer"]
        resp_offer = data["responder_offer"]

        if init_offer.owner == resp_offer.owner:
            raise serializers.ValidationError(
                "You cannot propose a barter deal using items you both own."
            )

        if init_offer.status != "ACTIVE" or resp_offer.status != "ACTIVE":
            raise serializers.ValidationError(
                "Both offers must be marked as AVAILABLE to initiate a deal."
            )
        duplicate_exists = (
            OfferDealModel.objects.filter(
                (Q(initiator_offer=init_offer) & Q(responder_offer=resp_offer))
                | (Q(initiator_offer=resp_offer) & Q(responder_offer=init_offer))
            )
            .filter(status__in=[DealStatus.PROPOSED, DealStatus.ACCEPTED])
            .exists()
        )

        if duplicate_exists:
            raise serializers.ValidationError(
                "A deal involving these exact two offers has already been proposed or finalized."
            )

        return data
