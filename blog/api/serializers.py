from rest_framework import serializers
from blog.models import Blog, Topic, Photo, Tag
from register.api.serializers import UserSerializer


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = "__all__"
    


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = "__all__"


class BlogSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False)
    class Meta:
        model = Blog
        fields = "__all__"
        

class BlogSerializerReadOnly(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    image = PhotoSerializer(read_only=True)
    class Meta:
        model = Blog
        fields = "__all__"
