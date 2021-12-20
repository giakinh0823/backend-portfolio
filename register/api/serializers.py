
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User, Group
from rest_framework import serializers
import json


class MyTokenObtainPairAdminSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        if self.user.is_superuser:
            data['user'] = json.dumps({
                "id": self.user.id,
                "username": self.user.username,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "email": self.user.email,
                "is_staff": self.user.is_staff,
                "is_active": self.user.is_active,
                "is_superuser": self.user.is_superuser,
                'groups': [g for g in self.user.groups.all()]
            })
            return data
        return {}


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'first_name', 'last_name',
                  'groups', 'is_staff', 'is_superuser', 'is_active']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
