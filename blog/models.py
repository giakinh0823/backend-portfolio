from django.db import models

# Create your models here.
import re
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField


class Photo(models.Model):
  image = CloudinaryField('image')
  url = models.CharField(max_length=255, blank=True, null=True)


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topic, related_name="topics")
    tags = models.ManyToManyField(Tag, related_name="tags")
    title = models.CharField(max_length=2000)
    description = models.CharField(max_length=2000)
    image = models.ForeignKey(Photo, on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField()
    is_remove = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
