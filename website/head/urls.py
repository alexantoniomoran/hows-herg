from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from head.api.constants import ADMIN_ENABLED
from head.api.views import MainPageView


urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path("api/", include("head.api.urls")),
    url("^$", MainPageView.as_view(), name="main-page",),
]

if ADMIN_ENABLED:
    urlpatterns.append(path("admin/", admin.site.urls))
