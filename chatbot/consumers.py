import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Group, Message
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        
        print(self.room_name)
        
        try:
            group = await sync_to_async(Group.objects.get)(id=self.room_name)
        except:
            user = await  sync_to_async(User.objects.get)(username='giakinh0823')
            group = await sync_to_async(Group.objects.create)(id=self.room_name, user_1=user)
            
        self.group = group
        
        # Join room group
        await self.channel_layer.group_add(
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
        print(data_json)
        message = data_json['message']
        
        try:
            user = data_json['user']
            user = await  sync_to_async(User.objects.get)(id=user['id'])    
            message = await sync_to_async(Message.objects.create)(group=self.group, user=user, message=message)
        except:
            user = await sync_to_async(User.objects.create)(username=f'user-{self.room_name}')
            self.group.user_2 = user
            self.group.save()
            message = await sync_to_async(Message.objects.create)(group=self.group, user=user, message=message,is_client=True)
        
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
                    "user" : user_dict,
                    "message": message.message,
                    "message_id": str(message.id),
                    "date": message.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                    "is_client": message.is_client,
                    "group": str(self.group.id),
                }
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        data = event['data']
        # Send message to WebSocket
        await self.send(text_data=json.dumps(data))
        
    
        