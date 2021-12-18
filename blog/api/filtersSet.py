import django_filters
from blog.models import Blog, Topic, Photo, Tag


class BlogFilter(django_filters.FilterSet):
    class Meta:
        model = Blog
        fields = ['title', 'slug', 'created_at', 'updated_at', 'topics', 'author', 'is_public', 'is_remove']


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
        
