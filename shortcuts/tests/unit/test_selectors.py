from unittest.mock import patch

from django.test import TestCase

from shortcuts.models import UrlShortcut
from shortcuts.selectors import get_url_shortcut


class GetUrlShortcutTest(TestCase):
    def setUp(self):
        self.random_url = "https://www.youtube.com/"
        self.random_code = "ABC123"

    @patch("shortcuts.models.generate_random_code")
    def test_shortcut_exists(self, mock_random_code):
        mock_random_code.return_value = self.random_code

        shortcut_obj = UrlShortcut.objects.create(target_url=self.random_url, code=self.random_code)
        self.assertEqual(get_url_shortcut(code=self.random_code), shortcut_obj)

    def test_shortcut_does_not_exist(self):
        self.assertIsNone(get_url_shortcut(code=self.random_code))
