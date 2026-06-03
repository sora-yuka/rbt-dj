from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Status(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    TRADED = "TRADED", "Traded"


class CategoryModel(models.Model):
    category = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.category


class OfferModel(models.Model):
    owner = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="offers"
    )
    title = models.CharField(max_length=150)
    description = models.TextField()
    category = models.ForeignKey(
        CategoryModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="offers",
    )
    desired_offer = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=50, choices=Status.choices, default=Status.ACTIVE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def offer_upload_to(instance, filename):
    return f"offers/offer_{instance.offer.id}/{filename}"


class OfferMediaModel(models.Model):
    offer = models.ForeignKey(
        OfferModel, on_delete=models.CASCADE, related_name="media"
    )
    file = models.FileField(upload_to=offer_upload_to, max_length=500)
