
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

# Tag admin


class ChatbotMessageAdminViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.filter(is_remove=False)
    serializer_class = MessageAdminSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = "__all__"
    
class ChatbotsMessagePublicViewSet(APIView):
    queryset = Message.objects.filter(is_remove=False)
    
    def get(self, request, format=None):
        query = self.filter_queryset(self.get_queryset())
        serializer = MessagePublicSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class ChatbotGroupAdminViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.filter(is_remove=False)
    serializer_class = GroupAdminSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = "__all__"
    
class ChatbotGroupPublicViewSet(APIView):
    queryset = Group.objects.filter(is_remove=False)
    
    def get(self, request, format=None):
        query = self.filter_queryset(self.get_queryset())
        serializer = GroupPublicSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
