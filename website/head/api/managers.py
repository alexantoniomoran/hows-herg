from django.db import models
from random import randint

from head.api.constants import TWILIO_DEFAULT_MESSAGES


class MessageBodyManager(models.Manager):
    def get_random_message_body(self, message_type):
        message_body = None
        body = TWILIO_DEFAULT_MESSAGES[message_type]

        message_bodies = self.filter(message_type=message_type)
        if message_bodies:
            message_id = randint(0, len(message_bodies) - 1)
            message_body = message_bodies[message_id]
            body = message_body.message

        return message_body, body
