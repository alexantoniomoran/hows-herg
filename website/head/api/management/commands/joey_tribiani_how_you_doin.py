from django.core.management.base import BaseCommand
from twilio.rest import Client

from head.api.constants import (
    MESSAGE_TO_SEND,
    TWILIO_ACCOUNT_SID,
    TWILIO_ACCOUNT_SID_TEST,
    TWILIO_AUTH_TOKEN,
    TWILIO_AUTH_TOKEN_TEST,
)
from head.api.models import MessageBody
from head.api.utils import save_message, send_twilio_message


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

    def send_daily_message(self, **options):
        message_body, body = MessageBody.objects.get_random_message_body(
            MESSAGE_TO_SEND
        )

        client = self.get_twilio_client(**options)
        if not options["test"]:
            payload = send_twilio_message(body, client, message_body)
            save_message(payload)

    def handle(self, *args, **options):
        self.send_daily_message(**options)
