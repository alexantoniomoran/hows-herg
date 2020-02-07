# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.contrib import admin
from head.api.models import MessageBody, MessageSent


class MessageBodyAdmin(admin.ModelAdmin):
    # fields = "__all__"
    list_display = ("id", "message")
    verbose_name = "Message Body"
    verbose_name_plural = "Message Bodies"


class MessageSentAdmin(admin.ModelAdmin):
    # fields = "__all__"
    list_display = ("id", "message_body", "status")


admin.site.register(MessageBody, MessageBodyAdmin)
admin.site.register(MessageSent, MessageSentAdmin)
