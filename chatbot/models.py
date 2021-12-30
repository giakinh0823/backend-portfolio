from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)   
    users = models.ManyToManyField(User, related_name='group_users')
    is_active = models.BooleanField(default=False)
    is_bot_run = models.BooleanField(default=True)
    is_remove = models.BooleanField(default=False)
    notis = models.ManyToManyField(User, related_name='noti_users')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    
class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_client = models.BooleanField(default=False)
    message = models.TextField()
    type_message = models.CharField(max_length=50, default='string')
    is_remove = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)    
