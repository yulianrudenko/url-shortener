from django.urls import reverse
from rest_framework import serializers

from shortcuts.models import UrlShortcut

class UrlShortcutSerializer(serializers.ModelSerializer):
    target_url = serializers.URLField(write_only=True)
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = UrlShortcut
        fields = [
            "target_url",
            "short_url"
        ]

    def get_short_url(self, obj: UrlShortcut):
        request = self.context["request"]
        path = reverse("shortcuts:shortcut-detail", args=[obj.code])
        short_url = request.build_absolute_uri(path)
        return short_url
