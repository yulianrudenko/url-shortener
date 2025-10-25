from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from shortcuts.serializers import UrlShortcutSerializer


class UrlShortcutSerializerTest(TestCase):
    def setUp(self):
        self.random_url = "https://www.youtube.com/"
        self.random_code = "ABC123"

    @patch("shortcuts.models.generate_random_code")
    def test_save_code_is_set_to_random_code(self, mock_random_code):
        mock_random_code.return_value = self.random_code
        factory = APIRequestFactory()
        url = reverse("shortcuts:shortcut-create")
        request = factory.get(url)

        serializer = UrlShortcutSerializer(
            data={"target_url": self.random_url}, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        shortcut_obj = serializer.save()
        expected_path = reverse("shortcuts:shortcut-detail", args=[shortcut_obj.code])
        self.assertEqual(shortcut_obj.target_url, self.random_url)
        self.assertEqual(
            serializer.data["short_url"], request.build_absolute_uri(expected_path)
        )
        mock_random_code.assert_called_once_with()
