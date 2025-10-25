from unittest.mock import patch

from django.test import TestCase

from shortcuts.models import UrlShortcut


class UrlShortcutTest(TestCase):
    def setUp(self):
        self.random_url = "https://www.youtube.com/"
        self.random_code = "ABC123"

    @patch("shortcuts.models.generate_random_code")
    def test_save_code_is_set_to_random_code(self, mock_random_code):
        mock_random_code.return_value = self.random_code

        shortcut_obj = UrlShortcut(target_url=self.random_url)
        shortcut_obj.save()
        shortcut_obj.refresh_from_db()
        self.assertEqual(shortcut_obj.code, self.random_code)
        mock_random_code.assert_called_once_with()

    @patch("shortcuts.models.generate_random_code")
    def test_save_code_is_ensured_to_be_unique(self, mock_random_code):
        new_unique_code = "ABC456"
        mock_random_code.side_effect = [self.random_code, self.random_code, new_unique_code]
        shortcut_obj = UrlShortcut.objects.create(target_url=self.random_url, code=self.random_code)
        self.assertEqual(shortcut_obj.code, self.random_code)
        self.assertEqual(mock_random_code.call_count, 1)

        shortcut_obj = UrlShortcut(target_url=self.random_url)
        shortcut_obj.save()
        shortcut_obj.refresh_from_db()
        self.assertEqual(shortcut_obj.code, new_unique_code)
        self.assertEqual(mock_random_code.call_count, 3)  # Second call worked
