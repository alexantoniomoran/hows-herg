import pytz

from twilio.twiml.messaging_response import MessagingResponse

from head.api.constants import (
    message_receive_body_dict,
    MESSAGE_RESPOND_BAD,
    MESSAGE_RESPOND_GOOD,
    NUM_MESSAGES_TO_SHOW,
    SEND_PHONE_NUMBER,
)
from head.api.models import MessageBody, MessageReceive, MessageSent


class MainPageMixin(object):
    def _format_date(self, date):
        return date.astimezone(pytz.timezone("US/Eastern")).strftime(
            "%-I:%M%p EST on %-m/%-d/%y"
        )

    def _get_sorted_messages(self):
        messages = []

        messages_from_herg = MessageReceive.objects.filter(
            message_from_number=SEND_PHONE_NUMBER
        )
        messages_to_herg = MessageSent.objects.filter(
            sent_type=MessageSent.SENT_FROM_WEBSITE
        )

        for qs in [messages_from_herg, messages_to_herg]:
            for message in qs:
                if hasattr(message, "sent_from_website_name"):
                    if message.sent_from_website_name:
                        messages.append(
                            {
                                "created_at": message.created_at,
                                "display_time": self._format_date(message.created_at),
                                "display_message": message.sent_from_website_text,
                                "display_message_from": message.sent_from_website_name,
                            }
                        )
                else:
                    messages.append(
                        {
                            "created_at": message.created_at,
                            "display_time": self._format_date(message.created_at),
                            "display_message": message.message_received,
                        }
                    )

        return sorted(messages, key=lambda x: x["created_at"])[::-1][
            :NUM_MESSAGES_TO_SHOW
        ]

    def _get_post_obj(self, error_msg, errors, field):
        text_message = self.request.POST.get(field)
        if not text_message:
            errors.append(error_msg)
        return text_message, errors


class MessageReceiveMixin(object):
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
