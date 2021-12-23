from rest_framework import serializers
from blog.models import Blog, Topic, Photo, Tag
from register.api.serializers import UserSerializer, UserPublicSerializer


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class TagPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = "__all__"


class TopicPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name', 'slug']


class BlogSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False)

    class Meta:
        model = Blog
        fields = "__all__"
        
        
class BlogAdminSerializerReadOnly(serializers.ModelSerializer):
    topics = TopicPublicSerializer(many=True, read_only=True)
    tags = TagPublicSerializer(many=True, read_only=True)
    author = UserPublicSerializer(read_only=True)
    image = PhotoSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = "__all__"


class BlogSerializerReadOnly(serializers.ModelSerializer):
    topics = TopicPublicSerializer(many=True, read_only=True)
    tags = TagPublicSerializer(many=True, read_only=True)
    author = UserPublicSerializer(read_only=True)
    image = PhotoSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'topics', 'tags', 'author',
                  'image', 'description', 'content', 'created_at', 'updated_at']
