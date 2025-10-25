from shortcuts.models import UrlShortcut


def get_url_shortcut(code: str) -> UrlShortcut | None:
    return UrlShortcut.objects.filter(code=code).first()
