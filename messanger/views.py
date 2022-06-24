from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from messanger.models import Message
from messanger.serializers import MessageSerializer


@api_view(['POST', 'GET'])
def messages(request):
    """
    Post a message | Get all user messages(redirect)
    """
    if request.method == 'POST':
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        return redirect('/messages/' + request.user.username)


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


@api_view(['GET', 'DELETE'])
def get_delete_message(request, pk):
    """
    Read or delete a message.
    """
    try:
        message = Message.objects.get(pk=pk)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        message.read = True
        message.save()
        serializer = MessageSerializer(message)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
