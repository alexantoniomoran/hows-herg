from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User as BaseUser

from head.api.forms import CustomAuthForm
from head.api.models import MessageBody, MessageReceive, MessageSent, Picture

admin.AdminSite.login_form = CustomAuthForm


@admin.register(MessageBody)
class MessageBodyAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "message_type")


@admin.register(MessageReceive)
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


@admin.register(MessageSent)
class MessageSentAdmin(admin.ModelAdmin):
    list_display = ("id", "message_sent", "created_at")


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    fields = ("image", "title", "description")
    list_display = ("title", "thumbnail_image", "description")
    readonly_fields = ("thumbnail_image",)


admin.site.unregister(BaseUser)


@admin.register(BaseUser)
class ChumpUserAdmin(UserAdmin):
    def has_change_permission(self, request, obj=None):
        print("GOT HERE!!!!")

        if request.user.is_super_user():
            return True
        else:
            return False
