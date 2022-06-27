from rest_framework.serializers import ModelSerializer

from messenger.models import Message


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'receiver', 'subject', 'msg_body', 'created_at', 'read_at', 'read')
