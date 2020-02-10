import pytz

from rest_framework import mixins, viewsets
from django.http import HttpResponse
from django.views.generic import TemplateView
from braces.views import CsrfExemptMixin
from twilio.twiml.messaging_response import MessagingResponse

from head.api.constants import (
    DEFAULT_DISPLAY_MESSAGE,
    message_receive_body_dict,
    MESSAGE_RESPOND_BAD,
    MESSAGE_RESPOND_GOOD,
    NUM_MESSAGES_TO_SHOW,
    NY_TIME_NOW,
    SEND_PHONE_NUMBER,
)
from head.api.models import MessageBody, MessageReceive


class MessageReceiveViewSet(
    CsrfExemptMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    authentication_classes = []

    def _create_object_payload(self, data):
        payload = {}
        for key in message_receive_body_dict:
            received_data = None
            if key in data:
                received_data = data[key][0]

            payload[message_receive_body_dict[key]] = received_data

        payload["message_received"] = payload["message_received"][:1024]
        return payload

    def _reply_to_sender(self, payload):
        resp = MessagingResponse()
        if not payload["message_received"]:
            message_body, body = MessageBody.objects.get_random_message_body(
                MESSAGE_RESPOND_BAD
            )
        else:
            message_body, body = MessageBody.objects.get_random_message_body(
                MESSAGE_RESPOND_GOOD
            )
        return resp, message_body, body

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        payload = self._create_object_payload(data)

        resp, message_body, body = self._reply_to_sender(payload)
        payload["message_response_sent"] = message_body

        message_received = MessageReceive(**payload)
        message_received.save()

        resp.message(body)
        return HttpResponse(resp)


class MainPageView(TemplateView):
    template_name = "main_page.html"

    def _format_date(self, date):
        return date.astimezone(pytz.timezone("US/Eastern")).strftime(
            "%-I:%M%p EST on %-m/%-d/%y"
        )

    def get_context_data(self, **kwargs):
        messages = MessageReceive.objects.filter(
            message_from_number=SEND_PHONE_NUMBER
        ).order_by("-created_at")[:NUM_MESSAGES_TO_SHOW]

        messages_list = []
        for message in messages:
            messages_list.append(
                {
                    "display_time": self._format_date(message.created_at),
                    "display_message": message.message_received,
                }
            )

        if not messages:
            messages_list.append(
                {
                    "display_time": self._format_date(NY_TIME_NOW),
                    "display_message": DEFAULT_DISPLAY_MESSAGE,
                }
            )

        kwargs["messages"] = messages_list
        return super(MainPageView, self).get_context_data(**kwargs)
