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
    is_public = models.BooleanField(default=False, null=True, blank=True)
    is_remove = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    is_public = models.BooleanField(default=False, null=True, blank=True)
    is_remove = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        qs = Topic.objects.filter(slug=slug)
        if qs:
            exists = qs.exists()
            if exists:
                self.slug = "%s-%s" % (slug, qs.first().id)
        else:
            self.slug = slug
        return super().save(*args, **kwargs)

        


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
    
    def save(self, *args, **kwargs):
        slug = slugify(self.title)
        qs = Topic.objects.filter(slug=slug)
        if qs:
            exists = qs.exists()
            if exists:
                self.slug = "%s-%s" % (slug, qs.first().id)
        else:
            self.slug = slug
        return super().save(*args, **kwargs)
