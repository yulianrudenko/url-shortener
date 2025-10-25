from django.db import models

from shortcuts.utils import generate_random_code


class UrlShortcut(models.Model):
    target_url = models.URLField()
    code = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        code = generate_random_code()
        while UrlShortcut.objects.filter(code=code).exists():
            code = generate_random_code()

        self.code = code
        return super().save(*args, **kwargs)
