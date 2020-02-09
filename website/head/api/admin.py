from django.contrib import admin
from head.api.models import MessageBody, MessageReceive, MessageSent


class MessageBodyAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "message_type")


class MessageReceiveAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "message_response_sent_message",
        "message_body",
        "created_at",
    )

    def message_response_sent_message(self, obj):
        if obj.message_response_sent:
            return obj.message_response_sent.message
        return ""


class MessageSentAdmin(admin.ModelAdmin):
    list_display = ("id", "message_body_text", "created_at")


admin.site.register(MessageBody, MessageBodyAdmin)
admin.site.register(MessageReceive, MessageReceiveAdmin)
admin.site.register(MessageSent, MessageSentAdmin)
