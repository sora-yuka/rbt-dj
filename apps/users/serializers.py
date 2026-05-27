from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import UserModel


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserModel
        fields = [
            "username",
            "phone_number",
            "password",
            "password_confirm",
            "profile_photo",
        ]

    def validate(self, attrs: dict) -> dict:
        password = attrs.get("password")
        password_confirm = attrs.pop("password_confirm")

        if password != password_confirm:
            raise serializers.ValidationError("Password do not match.")
        return attrs

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
