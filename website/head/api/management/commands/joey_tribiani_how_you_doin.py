from django.core.management.base import BaseCommand
from twilio.rest import Client

from head.api.constants import (
    MESSAGE_TO_SEND,
    SEND_PHONE_NUMBER,
    TWILIO_ACCOUNT_SID,
    TWILIO_ACCOUNT_SID_TEST,
    TWILIO_AUTH_TOKEN,
    TWILIO_AUTH_TOKEN_TEST,
    TWILIO_PHONE_NUMBER,
)
from head.api.models import MessageBody, MessageSent


class Command(BaseCommand):
    help = "Sends message to SEND_PHONE_NUMBER to ask about how they're feeling"

    def add_arguments(self, parser):
        parser.add_argument(
            "--test", action="store_true", help="Send test message",
        )

    def get_twilio_client(self, **options):
        if options["test"]:
            return Client(TWILIO_ACCOUNT_SID_TEST, TWILIO_AUTH_TOKEN_TEST)
        return Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    def get_payload(self, message):
        return {
            "message_sent": message.body,
            "status": message.status,
            "error_code": message.error_code,
            "error_message": message.error_message,
            "price": message.price,
            "price_unit": message.price_unit,
            "message_from_number": message.from_,
            "message_service_sid": message.messaging_service_sid,
            "sid": message.sid,
            "message_to_number": message.to,
        }

    def save_message(self, payload):
        message_sent = MessageSent(**payload)
        message_sent.save()

    def send_daily_message(self, **options):
        message_body, body = MessageBody.objects.get_random_message_body(
            MESSAGE_TO_SEND
        )

        client = self.get_twilio_client(**options)
        if not options["test"]:
            message = client.messages.create(
                to=SEND_PHONE_NUMBER, from_=TWILIO_PHONE_NUMBER, body=body,
            )
            payload = self.get_payload(message)
            payload["message_body"] = message_body
            self.save_message(payload)

    def handle(self, *args, **options):
        self.send_daily_message(**options)
