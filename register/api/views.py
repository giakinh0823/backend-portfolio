
from django.contrib.auth.models import User, Group
from rest_framework import serializers, status, viewsets, permissions, generics
from rest_framework.response import Response
from .serializers import UserSerializer, GroupSerializer, MyTokenObtainPairAdminSerializer, UserPublicSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.tokens import AccessToken


class MyTokenObtainPairAdminView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairAdminSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = "__all__"
    
# User cho người dùng
class UserPublicViewSet(generics.GenericAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = "__all__"
    
    def get(self, request, format=None):
        query = self.filter_queryset(self.get_queryset())
        serializer = UserPublicSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserFromTokenViewSet(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    
    def get_user(self, access_token):
        try:
            access_token_obj = AccessToken(access_token)
            user_id=access_token_obj['user_id']
            return user_id
        except:
            return None
            
    
    def post(self, request, format=None):
        try:
            access_token = request.data["access"]
        except:
            return Response({"error": "Không thể xác thực người dùng"}, status=status.HTTP_401_UNAUTHORIZED)
        if access_token:
            userId = self.get_user(access_token)
            if userId:
                user = User.objects.get(id=userId)
                serializers = UserSerializer(user) 
                return Response(serializers.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Không thể xác thực người dùng"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Không thể xác thực người dùng"}, status=status.HTTP_404_NOT_FOUND)
    
    
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]