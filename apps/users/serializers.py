from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import UserModel


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = UserModel
        fields = [
            "username",
            "phone_number",
            "password",
            "profile_photo",
        ]

    def create(self, validated_data: dict) -> UserModel:
        return UserModel.objects.create_user(**validated_data)


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            "id",
            "username",
            "phone_number",
            "profile_photo",
            "reputation_rating",
        ]
        read_only_fields = fields


class UserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            "id",
            "username",
            "phone_number",
            "profile_photo",
            "reputation_rating",
            "date_joined",
        ]
        read_only_fields = ["id", "reputation_rating", "date_joined"]
