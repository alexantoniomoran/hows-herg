from django.core.management.base import BaseCommand
from random import randint
from twilio.rest import Client

from head.api.constants import (
    SEND_PHONE_NUMBER,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_DEFAULT_MESSAGE,
    TWILIO_PHONE_NUMBER,
)
from head.api.models import MessageBody, MessageSent


class Command(BaseCommand):
    help = "Sends message to Herg to ask about how he's feeling"

    def get_message_body(self):
        message_body = None
        body = TWILIO_DEFAULT_MESSAGE

        message_bodies = MessageBody.objects.all()
        if message_bodies:
            message_id = randint(0, len(message_bodies) - 1)
            message_body = message_bodies[message_id]
            body = message_body.message

        return message_body, body

    def get_twilio_client(self):
        return Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    def save_message(self, message_body, message):
        message_sent = MessageSent(
            message_body=message_body,
            message_body_text=message.body,
            status=message.status,
            error_code=message.error_code,
            error_message=message.error_message,
            price=message.price,
            price_unit=message.price_unit,
        )
        message_sent.save()

    def send_daily_message(self):
        message_body, body = self.get_message_body()

        client = self.get_twilio_client()
        message = client.messages.create(
            to=SEND_PHONE_NUMBER, from_=TWILIO_PHONE_NUMBER, body=body,
        )

        self.save_message(message_body, message)

    def handle(self, *args, **options):
        self.send_daily_message()
