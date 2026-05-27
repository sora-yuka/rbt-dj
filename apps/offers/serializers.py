from rest_framework import serializers

from .models import Category, OfferModel, OfferMediaModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
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


class OfferWriteSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=True
    )
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=True,
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
