from django.contrib import admin
from head.api.models import MessageBody, MessageReceive, MessageSent


class MessageBodyAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "message_type")


class MessageReceiveAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "message_received",
        "message_response_sent_message",
        "created_at",
    )

    def message_response_sent_message(self, obj):
        if obj.message_response_sent:
            return obj.message_response_sent.message
        return ""

    message_response_sent_message.short_description = (
        "Message Sent Back to Confirm Feelings Received"
    )


class MessageSentAdmin(admin.ModelAdmin):
    list_display = ("id", "message_sent", "created_at")


admin.site.register(MessageBody, MessageBodyAdmin)
admin.site.register(MessageReceive, MessageReceiveAdmin)
admin.site.register(MessageSent, MessageSentAdmin)
