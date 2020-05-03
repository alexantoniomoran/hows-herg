from braces.views import CsrfExemptMixin
from django.http import HttpResponse
from django.views.generic import TemplateView
from rest_framework import mixins, viewsets
from twilio.rest import Client

from head.api.constants import (
    DEFAULT_DISPLAY_MESSAGE,
    NY_TIME_NOW,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    WEBSITE_GREETING,
    WEBSITE_MESSAGE_ERROR,
    WEBSITE_NAME_ERROR,
    WEBSITE_SUCCESS,
)
from head.api.mixins import MessageReceiveMixin, MainPageMixin
from head.api.models import MessageReceive, MessageSent
from head.api.utils import save_message, send_twilio_message


class MainPageView(CsrfExemptMixin, MainPageMixin, TemplateView):
    template_name = "main_page.html"

    def get_context_data(self, **kwargs):
        from_messages = self._get_messages_from()
        if not from_messages:
            from_messages.append(
                {
                    "display_time": self._format_date(NY_TIME_NOW),
                    "display_message": DEFAULT_DISPLAY_MESSAGE,
                }
            )

        to_messages = self._get_messages_to()
        if not to_messages:
            to_messages.append(
                {
                    "display_time": self._format_date(NY_TIME_NOW),
                    "display_message": "No texts sent :(",
                }
            )

        kwargs["from_messages"] = from_messages
        kwargs["to_messages"] = to_messages
        return super(MainPageView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        errors = []
        from_name, errors = self._get_post_obj(WEBSITE_NAME_ERROR, errors, "from_name")
        text_message, errors = self._get_post_obj(
            WEBSITE_MESSAGE_ERROR, errors, "text_message"
        )
        if errors:
            return self.render_to_response(
                self.get_context_data(
                    errors=errors, from_name=from_name, text_message=text_message
                )
            )

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        try:
            payload = send_twilio_message(
                f"{WEBSITE_GREETING} '{from_name}': {text_message}",
                client,
                sent_type=MessageSent.SENT_FROM_WEBSITE,
            )

            payload["sent_from_website_name"] = from_name
            payload["sent_from_website_text"] = text_message
            save_message(payload)
        except Exception as e:
            errors.append(str(e))

        return self.render_to_response(
            self.get_context_data(errors=errors, success=WEBSITE_SUCCESS)
        )


class MessageReceiveViewSet(
    CsrfExemptMixin,
    MessageReceiveMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        payload = self._create_object_payload(data)

        resp, message_body, body = self._reply_to_sender(payload)
        payload["message_response_sent"] = message_body

        message_received = MessageReceive(**payload)
        message_received.save()

        resp.message(body)
        return HttpResponse(resp)
