from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url

from head.api.constants import ADMIN_ENABLED
from head.api.views import MainPageView


urlpatterns = [
    path("api/", include("head.api.urls")),
    url("^$", MainPageView.as_view(), name="main-page",),
]


if ADMIN_ENABLED:
    urlpatterns.append(path("admin/", admin.site.urls))
