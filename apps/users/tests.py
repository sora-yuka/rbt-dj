from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.enroll_url = reverse("user_register")
        self.authenticate_url = reverse("token_obtain_pair")

        self.user_data = {
            "username": "testuser",
            "phone_number": "+996700111333",
            "password": "securepassword",
            "password_confirm": "securepassword",
        }

        self.existing_user = UserModel.objects.create_user(
            username="existinguser",
            phone_number="+996557124566",
            password="securepassword",
        )

    def test_user_registration_success(self):
        response = self.client.post(self.enroll_url, self.user_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("tokens", response.data)
        self.assertIn("access", response.data["tokens"])
        self.assertEqual(response.data["user"]["username"], self.user_data["username"])

        self.assertTrue(
            UserModel.objects.filter(phone_number=self.user_data["phone_number"])
        )

    def test_user_registration_duplicate_phone(self):
        self.user_data["phone_number"] = "+996557124566"
        response = self.client.post(self.enroll_url, self.user_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("phone_number", response.data)

    def test_user_login_success(self):
        credentials = {"phone_number": "+996557124566", "password": "securepassword"}
        response = self.client.post(self.authenticate_url, credentials, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_login_invalid(self):
        credentials = {"phone_number": "+996557124566", "password": "wrongpassword"}
        response = self.client.post(self.authenticate_url, credentials, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedEndpointTests(APITestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username="authuser",
            phone_number="+996700111333",
            password="securepassword",
            password_confirm="securepassword",
        )
        self.authenticate_url = reverse("token_obtain_pair")
        response = self.client.post(
            self.authenticate_url,
            {"phone_number": "+996700111333", "password": "securepassword"},
            format="json",
        )
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
