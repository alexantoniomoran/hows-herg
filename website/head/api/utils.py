from head.api.constants import (
    SEND_PHONE_NUMBER,
    TWILIO_PHONE_NUMBER,
)
from head.api.models import MessageSent


def get_payload(message, sent_type):
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
        "sent_type": sent_type,
    }


def save_message(payload):
    message_sent = MessageSent(**payload)
    message_sent.save()


def send_twilio_message(
    body, client, message_body=None, sent_type=MessageSent.SENT_FROM_TWILIO
):
    message = client.messages.create(
        to=SEND_PHONE_NUMBER, from_=TWILIO_PHONE_NUMBER, body=body,
    )
    payload = get_payload(message, sent_type)
    if message_body:
        payload["message_body"] = message_body
    return payload
