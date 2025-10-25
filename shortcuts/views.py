from django.http import HttpResponseRedirect
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.request import Request

from shortcuts.models import UrlShortcut
from shortcuts.selectors import get_url_shortcut
from shortcuts.serializers import UrlShortcutSerializer


class UrlShortcutCreateView(CreateAPIView):
    queryset = UrlShortcut.objects.all()
    serializer_class = UrlShortcutSerializer


class UrlShortcutDetailView(APIView):
    def get(self, request: Request, url_code: str):
        """Return full URL for provided shortcut."""
        shortcut_obj = get_url_shortcut(code=url_code)
        if shortcut_obj is None:
            raise NotFound(detail="URL nie istnieje")

        return HttpResponseRedirect(redirect_to=shortcut_obj.target_url)
