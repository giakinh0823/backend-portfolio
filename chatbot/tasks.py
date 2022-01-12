
from celery import shared_task
from celery.schedules import crontab
from backend.celery import app

from .chatbot import bot, LogicAdapter
from django.contrib.auth.models import User
from .models import Message, Group
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import random
from googletrans import Translator
from random import choice
from chatterbot.trainers import ListTrainer
from .models import Message, Group


translator = Translator()


@shared_task(name="bot_train")
def is_active_website():
    print("Start training bot")
    list_trainer = ListTrainer(bot.chatbot)
    groups = Group.objects.all()
    for group in groups:
        list_message = []
        messages = Message.objects.filter(group=group).order_by('-created_at')
        for message in messages:
            if message.is_client:
                list_message.append(str(message.message))
        list_trainer.train(list_message)

    return "Train bot sucessfully"


@shared_task(name="bot_remove")
def is_active_website():
    Group.objects.delete()
    return "Remove group sucessfully"


@shared_task(name="bot_support")
def bot_support(message_id, text):
    message = Message.objects.get(id=message_id)
    text_translate = translator.translate(text, dest='en').text
    print(text)
    try:
        response = bot.get_response(text_translate)
        print(response)
        message_process = translator.translate(str(
            response.text), dest='vi').text if "Fuck" not in response.text and "fuck" not in response.text and len(str(response.text).split(" ")) > 3 else response.text
        message.message = message_process
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
        message.message = "Tôi xin lỗi, nhưng tôi không hiểu ý bạn"
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
        return "Tôi xin lỗi, nhưng tôi không hiểu ý bạn"


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
