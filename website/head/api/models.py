from django.db import models
from django.db.models.deletion import SET_NULL

from head.api.constants import MESSAGE_TO_SEND, MESSAGE_TYPES
from head.api.managers import MessageBodyManager


class MessageBody(models.Model):
    message = models.CharField(max_length=239)
    message_type = models.CharField(
        max_length=100, choices=MESSAGE_TYPES, default=MESSAGE_TO_SEND
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = MessageBodyManager()

    class Meta:
        verbose_name = "Message Body"
        verbose_name_plural = "Message Bodies"


class MessageSent(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    message_body = models.ForeignKey(
        "messagebody",
        related_name="messages_sent",
        null=True,
        blank=True,
        on_delete=SET_NULL,
    )
    message_body_text = models.CharField(max_length=511, null=True, blank=True)
    message_from_number = models.CharField(max_length=16, null=True, blank=True)
    message_to_number = models.CharField(max_length=16, null=True, blank=True)

    status = models.CharField(max_length=31, null=True, blank=True)
    error_code = models.IntegerField(null=True, blank=True)
    error_message = models.CharField(max_length=255, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    price_unit = models.CharField(max_length=31, null=True, blank=True)
    message_service_sid = models.CharField(max_length=64, null=True, blank=True)
    sid = models.CharField(max_length=64, null=True, blank=True)


    class Meta:
        verbose_name = "Message Sent"
        verbose_name_plural = "Messages Sent"


class MessageReceive(models.Model):
    message_body = models.CharField(max_length=1024, null=True, blank=True)
    message_response_sent = models.ForeignKey(
        "messagebody",
        related_name="messages_received",
        null=True,
        blank=True,
        on_delete=SET_NULL,
    )

    message_from_number = models.CharField(max_length=16, null=True, blank=True)
    message_from_city = models.CharField(max_length=64, null=True, blank=True)
    message_from_state = models.CharField(max_length=2, null=True, blank=True)
    message_from_zip = models.CharField(max_length=16, null=True, blank=True)
    message_from_country = models.CharField(max_length=32, null=True, blank=True)
    message_to_number = models.CharField(max_length=16, null=True, blank=True)
    message_to_city = models.CharField(max_length=64, null=True, blank=True)
    message_to_state = models.CharField(max_length=2, null=True, blank=True)
    message_to_zip = models.CharField(max_length=16, null=True, blank=True)
    message_to_country = models.CharField(max_length=32, null=True, blank=True)

    account_sid = models.CharField(max_length=64, null=True, blank=True)
    message_sid = models.CharField(max_length=64, null=True, blank=True)
    number_of_segments = models.IntegerField(null=True, blank=True)
    sms_message_sid = models.CharField(max_length=64, null=True, blank=True)
    sms_sid = models.CharField(max_length=64, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "Message Received"
        verbose_name_plural = "Messages Received"
