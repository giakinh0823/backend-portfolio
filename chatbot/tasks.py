
from celery import shared_task
from .chatbot import bot, LogicAdapter
from django.contrib.auth.models import User
from .models import Message, Group
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import random

@shared_task(name="bot_support")
def bot_support(message_id, text):
    message = Message.objects.get(id=message_id)
    try:
        response = bot.get_response(text)
        print(response)
        message.message =str(response.text)
        message.save()
        user_dict = {
            "id": message.user.id,
            "username": message.user.username,
            "email": message.user.email,
            "first_name": message.user.first_name,
            "last_name": message.user.last_name,
        }
        room_group_name = 'chat_%s' % str(message.group.id)
        send_message(room_group_name, user_dict, message)
        return str(response.text)
    except:
        message.message ="I am sorry, but I do not understand"
        message.save()
        user_dict = {
            "id": message.user.id,
            "username": message.user.username,
            "email": message.user.email,
            "first_name": message.user.first_name,
            "last_name": message.user.last_name,
        }
        room_group_name = 'chat_%s' % str(message.group.id)
        send_message(room_group_name, user_dict, message)
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
