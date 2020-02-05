from django.db import models


class Messages(models.Model):
    SENT = "sent"
    RECEIVED = "received"

    created_at = models.DateTimeField("date published")
    message_type = models.Choices()
    text = models.CharField(max_length=200)


# https://docs.djangoproject.com/en/3.0/intro/tutorial02/
