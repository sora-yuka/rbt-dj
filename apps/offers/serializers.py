from rest_framework import serializers
from django.utils.timesince import timesince

from .models import CategoryModel, OfferModel, OfferMediaModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ["id", "category"]
        read_only_fields = fields


class OfferMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferMediaModel
        fields = ["id", "offer", "file"]
        read_only_fields = ["id"]


class OfferReadSerializer(serializers.ModelSerializer):
    media = OfferMediaSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = OfferModel
        fields = [
            "id",
            "owner",
            "title",
            "description",
            "category",
            "desired_offer",
            "status",
            "media",
            "created_at",
            "updated_at",
        ]

    # def to_representation(self, instance: OfferModel):
    #     representation = super().to_representation(instance)
    #     if instance.created_at:
    #         representation["created_at"] = instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
    #     if instance.updated_at:
    #         representation["time_since_update"] = f"{timesince(instance.updated_at)} ago"
    #         representation["updated_at"] =instance.updated_at.strftime("%B %d, %Y at %I:%M %p")
    #     return representation


class OfferWriteSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=CategoryModel.objects.all(), required=True
    )
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False,
    )

    class Meta:
        model = OfferModel
        fields = [
            "title",
            "description",
            "category",
            "desired_offer",
            "uploaded_images",
        ]

    def create(self, validated_data: dict) -> OfferModel:
        uploaded_images = validated_data.pop("uploaded_images", [])
        offer = OfferModel.objects.create(**validated_data)

        for image in uploaded_images:
            OfferMediaModel.objects.create(
                offer=offer,
                file=image,
            )
        return offer
