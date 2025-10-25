from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from shortcuts.models import UrlShortcut
from shortcuts.utils import CODE_SIZE


class UrlShortcutFlowTest(APITestCase):
    def setUp(self):
        self.create_endpoint_url = reverse("shortcuts:shortcut-create")
        self.get_detail_endpoint_url = lambda code: reverse(
            "shortcuts:shortcut-detail", args=[code]
        )
        self.random_url = "https://www.youtube.com/"

    def test_(self):
        # Create shortcut
        payload = {"target_url": self.random_url}
        response = self.client.post(self.create_endpoint_url, payload, format="json")
        shortcut_obj = UrlShortcut.objects.first()
        self.assertIsNotNone(shortcut_obj, "Shortcut was not created in database")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expected_path = reverse("shortcuts:shortcut-detail", args=[shortcut_obj.code])
        expected_url = response.wsgi_request.build_absolute_uri(expected_path)
        self.assertEqual(
            response.data, {"short_url": expected_url}
        )

        # Retrieve shortcut (redirect to URL works)
        response = self.client.get(self.get_detail_endpoint_url(shortcut_obj.code))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, shortcut_obj.target_url)

        # Verify DB
        self.assertEqual(shortcut_obj.target_url, self.random_url)
        self.assertIsNotNone(shortcut_obj.code)
        self.assertEqual(len(shortcut_obj.code), CODE_SIZE)
        self.assertIsNotNone(shortcut_obj.created_at)
