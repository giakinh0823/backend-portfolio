
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
from django.db.models import Q

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
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = "__all__"
    ordering_fields = ["id", "created_at"]
    
    def get_user(self, access_token):
        try:
            access_token_obj = AccessToken(access_token)
            user_id=access_token_obj['user_id']
            return user_id
        except:
            return None

    def get(self, request, format=None):
        access_token = request.headers['Authorization'].replace("Bearer","").strip()
        user_id = self.get_user(access_token)
        print(user_id)
        user = User.objects.get(id=user_id)
        groups = Group.objects.filter(is_remove=False, users__in=[user]).order_by('-created_at')
        query = self.filter_queryset(groups)
        for group in query:
            messages = Message.objects.filter(group=group, is_remove=False)
            group.messages = messages
        serializer = GroupPublicSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChatbotGroupDeatailPublicViewSet(APIView):
    permission_classes = [AllowAny]

    # def get(self, request, id, format=None):
    #     try:
    #         group = Group.objects.get(id=id, is_remove=False)
    #         messages = Message.objects.filter(group=group, is_remove=False)
    #         group.messages = messages
    #         serializer = GroupPublicSerializer(group)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     except Group.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, id, format=None):
        try:
            data = request.data
            try:
                user_id = data['user_id']
                group = Group.objects.get(id=id, is_remove=False)
                user = User.objects.get(id=user_id)
                user_in_group = group.users.all()
                user_in_group = user_in_group.filter(id=user_id)
                if user_in_group:
                    group.notis.remove(user)
                    group.save()
                    messages = Message.objects.filter(group=group, is_remove=False)
                    group.messages = messages
                    serializer = GroupPublicSerializer(group)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response({"error": "Không tìm thấy user"}, status=status.HTTP_404_NOT_FOUND)
            except:
                user_id = None
                return Response({"error": "Đang tìm user"}, status=status.HTTP_404_NOT_FOUND)
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
