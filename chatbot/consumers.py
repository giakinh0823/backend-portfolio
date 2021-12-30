import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Group, Message
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
import uuid
from datetime import datetime
from django.db.models import Q



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        try:
            group = await sync_to_async(Group.objects.get)(id=self.room_name)
            users = await sync_to_async(group.users.all)()
        except:
            group = None
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_message_error',
                    'error': {
                        "message": "Chatbot chưa được khởi tạo",
                    }
                }
            )
        
        self.group = group
        self.users = users

        if group:
        # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
        else:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data_json = json.loads(text_data)
        message = data_json['message']
        type_message = data_json['type_message']

        try:
            user = data_json['user']
            user = await sync_to_async(User.objects.get)(id=user['id'])
            message = await sync_to_async(Message.objects.create)(group=self.group, user=user, message=message, is_client=(not user.is_superuser), type_message=type_message)
        except:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_message_error',
                    'error': {
                        "message": "Không thể gửi tin nhắn",
                    }
                }
            )

        user_dict = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
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
        users = await sync_to_async(self.users.all)()
        noti_users = await sync_to_async(users.filter)(~Q(id=user.id))
        await sync_to_async(self.set_noti)(noti_users, user)
        self.group.created_at = datetime.now()
        await sync_to_async(self.group.save)()
        
    def set_noti(self, noti_users, user):
        self.group.notis.remove(user)
        self.group.notis.add(*noti_users)
        self.group.save()

    # Receive message from room group
    async def chat_message(self, event):
        data = event['data']
        # Send message to WebSocket
        await self.send(text_data=json.dumps(data))

    async def send_message_error(self, event):
        data = event['error']
        await self.send(text_data=json.dumps(data))
