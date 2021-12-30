from rest_framework import serializers
from chatbot.models import Group, Message
from register.api.serializers import UserSerializer, UserPublicSerializer
from register.api.serializers import UserPublicSerializer


class GroupAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

class MessageAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        
class GroupPublicSerializer(serializers.ModelSerializer):
    user_1 = UserPublicSerializer()
    user_2 = UserPublicSerializer()
    class Meta:
        model = Group
        fields = ("id", "user_1", "user_2", "is_bot_run")

class MessagePublicSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer()
    group = GroupPublicSerializer()
    class Meta:
        model = Message
        fields = ("id", "message", "is_client", "created_at", "user", "group")