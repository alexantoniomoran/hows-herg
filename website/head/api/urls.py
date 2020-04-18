from django.conf.urls import url
from head.api.views import MessageReceiveViewSet


urlpatterns = [
    url(
        "message_receive$",
        MessageReceiveViewSet.as_view({"post": "create"}),
        name="message-receive",
    ),
]
