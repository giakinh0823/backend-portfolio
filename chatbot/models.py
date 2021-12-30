from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    is_remove = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_client = models.BooleanField(default=False)
    message = models.TextField()
    is_remove = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)    
