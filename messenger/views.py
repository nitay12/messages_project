from datetime import datetime

from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from messenger.models import Message
from messenger.serializers import MessageSerializer


class MessagesView(APIView):
    def get(self, request):
        return redirect('user_messages', request.user.username)

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def all_user_messages(request, username):
    """
    Get all user messages
    """
    try:
        user = User.objects.get(username=username)
        if request.user != user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        user_messages = Message.objects.filter(receiver_id=user.pk)
        read_param = request.query_params.get('read')
        if read_param is not None:
            read = None
            if read_param == 'false':
                read = False
            elif read_param == 'true':
                read = True
            else:
                return Response(data={"read": ["Read param must be true/false."]}, status=status.HTTP_400_BAD_REQUEST)
            user_messages = Message.objects.filter(receiver_id=user.pk, read=read)

        serializer = MessageSerializer(user_messages, many=True)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class OneMessageView(APIView):
    def get(self, request, username, pk):
        user = get_object_or_404(User, username=username)
        message = get_object_or_404(Message, pk=pk)
        if request.user != user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if request.user != message.receiver:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if not message.read:
            message.read = True
            message.read_at = datetime.now()
            message.save()
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def delete(self, request, username, pk):
        user = get_object_or_404(User, username=username)
        message = get_object_or_404(Message, pk=pk)
        if request.user != user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if (request.user != message.receiver) | (request.user != message.sender):
            return Response(status=status.HTTP_403_FORBIDDEN)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
