import string

from django.test import TestCase

from shortcuts.utils import CODE_SIZE, generate_random_code


class GenerateRandomCodeTest(TestCase):
    def test_code_contains_only_letters_and_digits(self):
        code = generate_random_code()
        for ch in code:
            self.assertTrue(ch in (string.ascii_letters + string.digits))

        code = generate_random_code(size=100)
        for ch in code:
            self.assertTrue(ch in (string.ascii_letters + string.digits))

    def test_code_size(self):
        code = generate_random_code()
        self.assertEqual(len(code), CODE_SIZE)
