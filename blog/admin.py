from django.contrib import admin
from .models import Topic, Blog, Photo, Tag
# Register your models here.

admin.site.register(Topic)
admin.site.register(Blog)
admin.site.register(Photo)
admin.site.register(Tag)