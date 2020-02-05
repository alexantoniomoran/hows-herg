import os
from twilio.rest import Client

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]

client = Client(account_sid, auth_token)

client.messages.create(
    to=os.environ["MY_PHONE_NUMBER"],
    from_="+1233456788",
    body="test message",
)


# https://www.twilio.com/blog/2017/10/how-to-receive-and-respond-to-text-messages-in-python-with-django-and-twilio.html