from django.db import models
from django.db.models.deletion import SET_NULL


class MessageBody(models.Model):
    message = models.CharField(max_length=511)


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
    status = models.CharField(max_length=31, null=True, blank=True)
    error_code = models.IntegerField(null=True, blank=True)
    error_message = models.CharField(max_length=255, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    price_unit = models.CharField(max_length=31, null=True, blank=True)
