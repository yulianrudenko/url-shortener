from rest_framework import serializers

from shortcuts.models import UrlShortcut

class UrlShortcutSerializer(serializers.ModelSerializer):
    code = serializers.CharField(read_only=True)

    class Meta:
        model = UrlShortcut
        fields = [
            "target_url",
            "code",
        ]
