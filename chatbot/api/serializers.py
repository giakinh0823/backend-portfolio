from rest_framework import serializers
from chatbot.models import Group, Message
from register.api.serializers import UserSerializer, UserPublicSerializer
from register.api.serializers import UserPublicSerializer


class MessagePublicGroupSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer()
    class Meta:
        model = Message
        fields = ("id", "message", "is_client", "created_at", "user")

class GroupAdminSerializer(serializers.ModelSerializer):
    messages = MessagePublicGroupSerializer(many=True, read_only=True)
    class Meta:
        model = Group
        fields = "__all__"

class MessageAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        



class GroupPublicSerializer(serializers.ModelSerializer):
    users = UserPublicSerializer(many=True, read_only=True)
    id = serializers.UUIDField(format="hex_verbose")
    messages = MessagePublicGroupSerializer(many=True, read_only=True)
    class Meta:
        model = Group
        fields = ("id", "users", "is_bot_run", "messages")


class MessagePublicSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer()
    group = GroupPublicSerializer()
    class Meta:
        model = Message
        fields = ("id", "message", "is_client", "created_at", "user", "group")
        