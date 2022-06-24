from rest_framework.serializers import ModelSerializer

from messanger.models import Message


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ('receiver', 'subject', 'msg_body', 'created_at', 'read_at', 'read')
