
from blog.forms import PhotoForm
from blog.models import Blog, Photo, Tag, Topic
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters

from .serializers import GroupAdminSerializer, GroupPublicSerializer, MessagePublicSerializer, MessageAdminSerializer
from chatbot.models import Group, Message
from rest_framework_simplejwt.tokens import AccessToken
import uuid

# Tag admin


class ChatbotMessageAdminViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.filter(is_remove=False)
    serializer_class = MessageAdminSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = "__all__"


class ChatbotsMessagePublicViewSet(generics.GenericAPIView):
    queryset = Message.objects.filter(is_remove=False)
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = "__all__"

    def get(self, request, format=None):
        query = self.filter_queryset(self.get_queryset())
        serializer = MessagePublicSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChatbotGroupAdminViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.filter(is_remove=False).order_by('-created_at')
    serializer_class = GroupAdminSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = "__all__"
    ordering_fields = ["id", "created_at"]


class ChatbotGroupAdminCustomViewSet(generics.GenericAPIView):
    queryset = Group.objects.filter(is_remove=False).order_by('-created_at')
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = "__all__"
    ordering_fields = ["id", "created_at"]

    def get(self, request, format=None):
        groups = self.get_queryset()
        query = self.filter_queryset(groups)
        for group in query:
            messages = Message.objects.filter(group=group, is_remove=False)
            group.messages = messages
        serializer = GroupPublicSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChatbotGroupDeatailPublicViewSet(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id, format=None):
        try:
            group = Group.objects.get(id=id, is_remove=False)
            messages = Message.objects.filter(group=group, is_remove=False)
            group.messages = messages
            serializer = GroupPublicSerializer(group)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, id, format=None):
        try:
            data = request.data
            user_id = data['user_id']
            group = Group.objects.get(id=id, is_remove=False)
            user_in_group = group.users.all(id=user_id)
            if user_in_group:
                messages = Message.objects.filter(group=group, is_remove=False)
                group.messages = messages
                serializer = GroupPublicSerializer(group)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "Không tìm thấy user"}, status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ChatbotGroupJoinViewSet(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        try:
            group = Group.objects.create()
            data = request.data
            try:
                userID = data['user_id']
                user = User.objects.get(id=userID)
            except:
                user = None
            if user:
                group.users.add(request.user)
                group.save()
            else:
                user = User.objects.create(username=str(uuid.uuid4()))
                group.users.add(request.user)
                group.save()

            return Response({"chatbot_id": str(group.id), "user": str(user.username)}, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
