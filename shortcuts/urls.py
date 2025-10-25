from django.urls import path

from shortcuts import views

app_name = "shortcuts"

urlpatterns = [
    path("shrt/", views.UrlShortcutCreateView.as_view(), name="shortcut-create"),
    path("shrt/<slug:url_code>", views.UrlShortcutDetailView.as_view(), name="shortcut-detail")
]
