import django_filters
from blog.models import Blog, Topic, Photo, Tag


class BlogFilter(django_filters.FilterSet):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'created_at', 'updated_at',
                  'topics', 'topics__name', 'topics__slug', 'tags', 'tags__name', 'author__username']


class TopicFilter(django_filters.FilterSet):
    class Meta:
        model = Topic
        fields = ['name', 'slug', 'is_remove']


class PhotoFilter(django_filters.FilterSet):
    class Meta:
        model = Photo
        fields = ['id']


class TagFilter(django_filters.FilterSet):
    class Meta:
        model = Tag
        fields = ['name']
