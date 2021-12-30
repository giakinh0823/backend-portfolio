from django.contrib import admin

# Register your models here.

from .models import Group, Message

admin.site.register(Group)
admin.site.register(Message)
