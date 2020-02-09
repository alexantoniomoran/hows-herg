from rest_framework import mixins, viewsets
from django.http import HttpResponse
from braces.views import CsrfExemptMixin

from twilio.twiml.messaging_response import MessagingResponse

from head.api.constants import (
    message_receive_body_dict,
    MESSAGE_RESPOND_BAD,
    MESSAGE_RESPOND_GOOD,
)
from head.api.models import MessageBody, MessageReceive


class MessageReceiveViewSet(
    CsrfExemptMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    authentication_classes = []

    def _create_object_payload(self, data):
        payload = {}
        for key in message_receive_body_dict:
            received_data = None
            if key in data:
                received_data = data[key]

            payload[message_receive_body_dict[key]] = received_data

        return payload

    def _reply_to_sender(self, payload):
        resp = MessagingResponse()
        if not payload["message_body"]:
            message_body, body = MessageBody.objects.get_random_message_body(
                MESSAGE_RESPOND_BAD
            )
        else:
            message_body, body = MessageBody.objects.get_random_message_body(
                MESSAGE_RESPOND_GOOD
            )
        return resp, message_body, body

    def create(self, request, *args, **kwargs):
        import pdb; pdb.set_trace()  #########################
        data = dict(request.data)
        payload = self._create_object_payload(data)

        resp, message_body, body = self._reply_to_sender(payload)
        payload["message_response_sent"] = message_body

        message_received = MessageReceive(payload)
        message_received.save()

        resp.message(body)
        return HttpResponse(resp)
