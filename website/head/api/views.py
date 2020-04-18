import pytz

from braces.views import CsrfExemptMixin
from django.http import HttpResponse
from django.views.generic import TemplateView
from rest_framework import mixins, viewsets
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from head.api.constants import (
    DEFAULT_DISPLAY_MESSAGE,
    HERG_GREETING,
    message_receive_body_dict,
    MESSAGE_RESPOND_BAD,
    MESSAGE_RESPOND_GOOD,
    NUM_MESSAGES_TO_SHOW,
    NY_TIME_NOW,
    SEND_PHONE_NUMBER,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
)
from head.api.models import MessageBody, MessageReceive, MessageSent
from head.api.utils import save_message, send_twilio_message


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


class MainPageView(CsrfExemptMixin, TemplateView):
    template_name = "main_page.html"

    def _format_date(self, date):
        return date.astimezone(pytz.timezone("US/Eastern")).strftime(
            "%-I:%M%p EST on %-m/%-d/%y"
        )

    def _get_sorted_messages(self):
        messages = []

        messages_from_herg = MessageReceive.objects.filter(
            message_from_number=SEND_PHONE_NUMBER
        )
        for message in messages_from_herg:
            messages.append(
                {
                    "created_at": message.created_at,
                    "display_time": self._format_date(message.created_at),
                    "display_message": message.message_received,
                }
            )

        messages_to_herg = MessageSent.objects.filter(
            sent_type=MessageSent.SENT_FROM_WEBSITE
        )
        for message in messages_to_herg:
            try:
                split_message = message.message_sent.split(HERG_GREETING[1:])
                message_from, message_sent = split_message[1].split("':")
                messages.append(
                    {
                        "created_at": message.created_at,
                        "display_time": self._format_date(message.created_at),
                        "display_message": message_sent.rstrip(),
                        "display_message_from": message_from[2:].rstrip(),
                    }
                )
            except:
                continue

        return sorted(messages, key=lambda x: x["created_at"])[::-1][:NUM_MESSAGES_TO_SHOW]

    def get_context_data(self, **kwargs):
        messages_list = self._get_sorted_messages()
        if not messages_list:
            messages_list.append(
                {
                    "display_time": self._format_date(NY_TIME_NOW),
                    "display_message": DEFAULT_DISPLAY_MESSAGE,
                }
            )

        kwargs["messages"] = messages_list
        return super(MainPageView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        errors = []

        from_name = self.request.POST.get("from_name")
        if not from_name:
            errors.append("Seriously? Tell Herg who you are.")

        text_message = self.request.POST.get("text_message")
        if not text_message:
            errors.append("Don't waste Herg's time with a blank text!")

        if errors:
            return self.render_to_response(
                self.get_context_data(
                    errors=errors, from_name=from_name, text_message=text_message
                )
            )

        try:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

            body = f"{HERG_GREETING} '{from_name}': {text_message}"
            payload = send_twilio_message(body, client, sent_type=MessageSent.SENT_FROM_WEBSITE)
            save_message(payload)
        except Exception as e:
            errors.append(str(e))

        return self.render_to_response(
            self.get_context_data(
                errors=errors, success="Sent your message to King Hergis!"
            )
        )
