from django.db import models

# Create your models here.
import re
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField
from autoslug import AutoSlugField


class Photo(models.Model):
    image = CloudinaryField('image')
    url = models.CharField(max_length=255, blank=True, null=True)


class Tag(models.Model):
    name = models.CharField(max_length=255)
    is_public = models.BooleanField(default=False, null=True, blank=True)
    is_remove = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = AutoSlugField(populate_from='name', unique=True, null=True, blank=True)
    is_public = models.BooleanField(default=False, null=True, blank=True)
    is_remove = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topic, related_name="topics")
    tags = models.ManyToManyField(Tag, related_name="tags")
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ForeignKey(
        Photo, on_delete=models.CASCADE, blank=True, null=True)
    slug = AutoSlugField(populate_from='title', unique=True, null=True, blank=True)
    content = models.TextField()
    is_remove = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
