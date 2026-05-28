from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    username = models.CharField(max_length=150)
    phone_number = models.CharField(unique=True)
    profile_photo = models.ImageField(upload_to="profile-pics/", blank=True, null=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return f"{self.username} (id={self.id})"
