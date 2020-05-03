import os

from datetime import datetime


ADMIN_ENABLED = bool(os.getenv("ADMIN_ENABLED", True))

SEND_PHONE_NUMBER = os.environ["SEND_PHONE_NUMBER"]

TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_ACCOUNT_SID_TEST = os.environ["TWILIO_ACCOUNT_SID_TEST"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_AUTH_TOKEN_TEST = os.environ["TWILIO_AUTH_TOKEN_TEST"]
TWILIO_PHONE_NUMBER = os.environ["TWILIO_PHONE_NUMBER"]

NUM_MESSAGES_TO_SHOW = int(os.getenv("NUM_MESSAGES_TO_SHOW", "7"))

message_receive_body_dict = {
    "AccountSid": "account_sid",
    "Body": "message_received",
    "From": "message_from_number",
    "FromCity": "message_from_city",
    "FromCountry": "message_from_country",
    "FromState": "message_from_state",
    "FromZip": "message_from_zip",
    "MessageSid": "message_sid",
    "NumSegments": "number_of_segments",
    "SmsMessageSid": "sms_message_sid",
    "SmsSid": "sms_sid",
    "To": "message_to_number",
    "ToCity": "message_to_city",
    "ToCountry": "message_to_country",
    "ToState": "message_to_state",
    "ToZip": "message_to_zip",
}

MESSAGE_TO_SEND = "send"
MESSAGE_RESPOND_BAD = "respond_bad"
MESSAGE_RESPOND_GOOD = "respond_good"
MESSAGE_TYPES = (
    (MESSAGE_TO_SEND, "Send"),
    (MESSAGE_RESPOND_BAD, "Respond to Bad Message"),
    (MESSAGE_RESPOND_GOOD, "Respond to Good Message"),
)

TWILIO_DEFAULT_MESSAGE_SEND = "Hey bud, how ya feeling today?"
TWILIO_DEFAULT_MESSAGE_RESPOND_BAD = (
    "Wasn't able to parse that message bud, maybe try again?"
)
TWILIO_DEFAULT_MESSAGE_RESPOND_GOOD = "Feelings received boss!"

TWILIO_DEFAULT_MESSAGES = {
    MESSAGE_TO_SEND: TWILIO_DEFAULT_MESSAGE_SEND,
    MESSAGE_RESPOND_BAD: TWILIO_DEFAULT_MESSAGE_RESPOND_BAD,
    MESSAGE_RESPOND_GOOD: TWILIO_DEFAULT_MESSAGE_RESPOND_GOOD,
}

NY_TIME_NOW = datetime.utcnow().replace(microsecond=0, tzinfo=None)
DEFAULT_DISPLAY_MESSAGE = "Herg has no feelings to report :'("

WEBSITE_GREETING = "Herg! You've got a text from"
WEBSITE_MESSAGE_ERROR = "Don't waste Herg's time with a blank text!"
WEBSITE_NAME_ERROR = "Seriously? Tell Herg who you are."
WEBSITE_SUCCESS = "Yay! Your message was sent to King Hergis!"
