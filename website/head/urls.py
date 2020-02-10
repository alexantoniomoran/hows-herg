from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url

from head.api.views import MainPageView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("head.api.urls")),
    url("^$", MainPageView.as_view(), name="main-page",),
]
