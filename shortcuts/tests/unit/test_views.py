from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from shortcuts.models import UrlShortcut


class UrlShortcutCreateViewTest(APITestCase):
    def setUp(self):
        self.endpoint_url = reverse("shortcuts:shortcut-create")
        self.random_url = "https://www.youtube.com/"
        self.random_code = "ABC123"

    def test_invalid_url_provided(self):
        payload = {"target_url": "invalid"}
        response = self.client.post(self.endpoint_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(UrlShortcut.objects.first())
        self.assertEqual(
            response.data,
            {"target_url": [ErrorDetail(string="Enter a valid URL.", code="invalid")]},
        )

    @patch("shortcuts.models.generate_random_code")
    def test_create_shortcut(self, mock_random_code):
        mock_random_code.return_value = self.random_code

        payload = {"target_url": self.random_url}
        response = self.client.post(self.endpoint_url, payload, format="json")

        shortcut_obj = UrlShortcut.objects.first()
        self.assertIsNotNone(shortcut_obj, "Shortcut was not created")
        self.assertEqual(shortcut_obj.target_url, self.random_url)
        self.assertEqual(shortcut_obj.code, self.random_code)
        self.assertIsNotNone(shortcut_obj.code)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data, {"target_url": self.random_url, "code": shortcut_obj.code}
        )


class UrlShortcutDetailView(APITestCase):
    def setUp(self):
        self.get_endpoint_url = lambda code: reverse(
            "shortcuts:shortcut-detail", args=[code]
        )
        self.random_url = "https://www.youtube.com/"

    def test_shortcut_exists_and_redirect_works(self):
        shortcut_obj = UrlShortcut.objects.create(target_url=self.random_url)
        response = self.client.get(self.get_endpoint_url(shortcut_obj.code))

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, shortcut_obj.target_url)

    def test_shortcut_does_not_exist(self):
        random_code = "ABC123"
        response = self.client.get(self.get_endpoint_url(random_code))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data,
            {"detail": ErrorDetail(string="URL nie istnieje", code="not_found")},
        )
