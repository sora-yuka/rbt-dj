from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class UserModel(AbstractUser):
    username = models.CharField(max_length=150)
    phone_number = models.CharField(unique=True)
    profile_photo = models.ImageField(upload_to="profile-pics/", blank=True, null=True)
    reputation_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=5.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(5.00)],
    )

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return f"{self.username} (id={self.id})"
