
from celery import shared_task
from .chatbot import bot, LogicAdapter
from django.contrib.auth.models import User
from .models import Message, Group
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import random

@shared_task(name="bot_support")
def bot_support(group_id, message):
    try:
        response = bot.get_response(message)
        print(response)
        user = User.objects.get(username="giakinh0823")
        group = Group.objects.get(id=group_id)
        message = Message.objects.create(
            group=group, user=user, message=str(response.text), is_client=False, type_message="string")
        user_dict = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        room_group_name = 'chat_%s' % str(group.id)
        send_message(room_group_name, user_dict, message)
        return str(response.text)
    except:
        return "I am sorry, but I do not understand."


def send_message(room_group_name, user_dict, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            'type': 'chat_message',
            'data': {
                "user": user_dict,
                "message": message.message,
                "type_message": message.type_message,
                "id": str(message.id),
                "created_at": message.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                "is_client": message.is_client,
            }
        }
    )
