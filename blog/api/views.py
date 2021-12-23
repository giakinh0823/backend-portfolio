
from blog.forms import PhotoForm
from blog.models import Blog, Photo, Tag, Topic
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters

from .filtersSet import BlogFilter, PhotoFilter, TagFilter, TopicFilter
from .pageSerializers import ResultsSetPagination, StandardResultsSetPagination
from .serializers import (BlogSerializer, BlogSerializerReadOnly,
                          PhotoSerializer, TagSerializer, TopicSerializer, TagPublicSerializer, TopicPublicSerializer, BlogAdminSerializerReadOnly)
import cloudinary

#Tag admin
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.filter(is_remove=False)
    serializer_class = TagSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filter_class = TagFilter
    filterset_fields = "__all__"
    

# Tag cho người dùng
class TagPublicViewSet(generics.GenericAPIView):
    queryset = Tag.objects.filter(is_remove=False, is_public=True)
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filter_class = TagFilter
    filterset_fields = "__all__"
    ordering_fields = ['title', 'created_at'] 

    def get(self, request, format=None):
        query = self.filter_queryset(self.get_queryset())
        serializer = TagPublicSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TagRemoveAllViewSet(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, format=None):
        tags = Tag.objects.filter(is_remove=False)
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request, format=None):
        data = request.data
        if data:
            for item in data:
                try:
                    tag = Tag.objects.get(id=item)
                    if tag:
                        tag.is_remove = True
                        tag.save()
                        # tag.delete()
                except:
                    return Response({"error": "Có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)
            return Response({"success": "Xóa tag thành công"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Đã có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)
        

class TagRemoveForeverViewSet(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, format=None):
        tags = Tag.objects.filter(is_remove=True)
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request, format=None):
        data = request.data
        if data:
            for item in data:
                try:
                    tag = Tag.objects.get(id=item)
                    if tag:
                        tag.delete()
                except:
                    return Response({"error": "Có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)
            return Response({"success": "Xóa tag thành công"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Đã có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)
        
class TagAdminTrashViewSet(generics.GenericAPIView):
    queryset = Tag.objects.filter(is_remove=True)
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filter_class =TagFilter
    filterset_fields = "__all__"
    ordering_fields = ['name']

    permission_classes = [IsAdminUser]
    def get(self, request, format=None):
        query = self.filter_queryset(self.get_queryset())
        serializer = TagSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        data = request.data
        if data:
            for item in data:
                try:
                    tag = Tag.objects.get(id=item)
                    if tag:
                        tag.is_remove = False
                        tag.save()
                        # blog.delete()
                except:
                    return Response({"error": "Có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)
            return Response({"success": "Restore tag thành công"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Đã có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)
    
    
#Photo admin
class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filter_class = PhotoFilter
    filterset_fields = "__all__"
    ordering_fields = ["id"]
    

#Upload photo
class PhotoUpload(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, format=None):
        photos = Photo.objects.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        context = dict( backend_form = PhotoForm())
        form = PhotoForm(request.POST, request.FILES)
        context['posted'] = form.instance
        if form.is_valid():
            data = form.save()
            data.url = data.image.url
            data.save()
            return Response({"success":"Tải hình ảnh thành công", "url": str(data.image.url) },status=status.HTTP_201_CREATED)
        return Response({"error": "Đã có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)
    
class PhotoUploadDetail(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request,pk, format=None):
        photo = Photo.objects.get(id=pk)
        if photo:
            serializer = PhotoSerializer(photo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Đã có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)
            
            
    def delete(self, request,pk, format=None):
        photo = Photo.objects.get(id=pk)
        if photo:
            cloudinary.uploader.destroy(photo.image.public_id, invalidate=True)
            photo.delete()
            return Response({"success":"Xóa hình ảnh thành công"},status=status.HTTP_200_OK)
        return Response({"error": "Đã có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)
    
class PhotoRemove(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, format=None):
        photos = Photo.objects.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        data = request.data
        if data:
            try:
                for item in data:
                    id = int(item["id"])
                    try:
                        photo = Photo.objects.get(id=id)
                        if photo:
                            cloudinary.uploader.destroy(photo.image.public_id, invalidate=True)
                            photo.delete()
                    except:
                        photo = None
                return Response({"success":"Xóa hình ảnh thành công"},status=status.HTTP_200_OK)
            except:
                return Response({"error": "Đã có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Đã có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)
            

# Topic cho admin
class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.filter(is_remove=False)
    serializer_class = TopicSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filter_class = TopicFilter
    filterset_fields = "__all__"
    
    
class TopicDetailViewSet(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request,slug, format=None):
        try:
            topic = Topic.objects.get(slug=slug)
            if topic:
                serializer = TopicSerializer(topic)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "Không tìm thấy topic"},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Đã có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)

class TopicRemoveViewSet(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request,pk, format=None):
        try:
            topic = Topic.objects.get(id=pk)
            if topic:
                serializer = TopicSerializer(topic)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "Không tìm thấy topic"},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Đã có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request,pk, format=None):
        try:
            topic = Topic.objects.get(id=pk)
            if topic:
                topic.is_remove = True
                topic.save()
                # topic.delete()
                serializer = TopicSerializer(topic)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "Không tìm thấy topic"},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Đã có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)
        

class TopicRemoveAllViewSet(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, format=None):
        topics = Topic.objects.filter(is_remove=False)
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request, format=None):
        data = request.data
        if data:
            for item in data:
                try:
                    topic = Topic.objects.get(id=item)
                    if topic:
                        topic.is_remove = True
                        topic.save()
                        # topic.delete()
                except:
                    return Response({"error": "Có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)
            return Response({"success": "Xóa topic thành công"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Đã có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)
        
        
        
class TopicRemoveForeverViewSet(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, format=None):
        topics = Topic.objects.filter(is_remove=True)
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request, format=None):
        data = request.data
        if data:
            for item in data:
                try:
                    topic = Topic.objects.get(id=item)
                    if topic:
                        topic.delete()
                except:
                    return Response({"error": "Có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)
            return Response({"success": "Xóa topic thành công"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Đã có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)
        
class TopicAdminTrashViewSet(generics.GenericAPIView):
    queryset = Topic.objects.filter(is_remove=True)
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filter_class =TopicFilter
    filterset_fields = "__all__"
    ordering_fields = ['name']

    def get(self, request, format=None):
        query = self.filter_queryset(self.get_queryset())
        serializer = TopicSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        data = request.data
        if data:
            for item in data:
                try:
                    topic = Topic.objects.get(id=item)
                    if topic:
                        topic.is_remove = False
                        topic.save()
                        # blog.delete()
                except:
                    return Response({"error": "Có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)
            return Response({"success": "Restore topic thành công"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Đã có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)
        
        

# Topic cho người dùng
class TopicPublicViewSet(generics.ListAPIView):
    queryset = Topic.objects.filter(is_remove=False, is_public=True)
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filter_class = TopicFilter
    filterset_fields = "__all__"
    ordering_fields = ['name']

    def get(self, request, format=None):
        query = self.filter_queryset(self.get_queryset())
        serializer = TopicPublicSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Blog cho admin
class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.filter(is_remove=False)
    serializer_class = BlogSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filter_class = BlogFilter
    filterset_fields = "__all__"
    ordering_fields = ['title', 'created_at']


# Blog cho người dùng
class BlogPublicViewSet(generics.GenericAPIView):
    queryset = Blog.objects.filter(is_remove=False, is_public=True)
    permission_classes = [AllowAny]
    pagination_class = ResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filter_class =BlogFilter
    filterset_fields = "__all__"
    ordering_fields = ['title', 'created_at']
    

    def get(self, request, format=None):
        query = self.filter_queryset(self.get_queryset())
        paginate_queryset = self.paginate_queryset(query)
        serializer = BlogSerializerReadOnly(paginate_queryset, many=True)
        return self.get_paginated_response(serializer.data)
    
# admin
class BlogAdminViewSet(generics.GenericAPIView):
    queryset = Blog.objects.filter(is_remove=False).order_by('-created_at')
    permission_classes = [IsAdminUser]
    pagination_class = ResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filter_class =BlogFilter
    filterset_fields = "__all__"
    ordering_fields = ['title', 'created_at']
    

    def get(self, request, format=None):
        query = self.filter_queryset(self.get_queryset())
        paginate_queryset = self.paginate_queryset(query)
        serializer = BlogAdminSerializerReadOnly(paginate_queryset, many=True)
        return self.get_paginated_response(serializer.data)
    
# Trash Blog
class BlogAdminTrashViewSet(generics.GenericAPIView):
    queryset = Blog.objects.filter(is_remove=True).order_by('-updated_at')
    permission_classes = [IsAdminUser]
    pagination_class = ResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filter_class =BlogFilter
    filterset_fields = "__all__"
    ordering_fields = ['title', 'created_at']
    

    def get(self, request, format=None):
        query = self.filter_queryset(self.get_queryset())
        paginate_queryset = self.paginate_queryset(query)
        serializer = BlogSerializerReadOnly(paginate_queryset, many=True)
        return self.get_paginated_response(serializer.data)
    
    def post(self, request, format=None):
        data = request.data
        if data:
            for item in data:
                try:
                    blog = Blog.objects.get(id=item)
                    if blog:
                        blog.is_remove = False
                        blog.save()
                        # blog.delete()
                except:
                    return Response({"error": "Có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)
            return Response({"success": "Restore blog thành công"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Đã có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)


class BlogDetailViewSet(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request,slug, format=None):
        try:
            blog = Blog.objects.get(slug=slug)
            if blog:
                serializer = BlogSerializerReadOnly(blog)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "Không tìm thấy topic"},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Đã có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)

class BlogRemoveAllViewSet(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, format=None):
        blogs = Blog.objects.filter(is_remove=False)
        serializer = TopicSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request, format=None):
        data = request.data
        if data:
            for item in data:
                try:
                    blog = Blog.objects.get(id=item)
                    if blog:
                        blog.is_remove = True
                        blog.save()
                        # blog.delete()
                except:
                    return Response({"error": "Có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)
            return Response({"success": "Xóa blog thành công"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Đã có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)
        

class BlogRemoveForeverViewSet(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, format=None):
        blogs = Blog.objects.filter(is_remove=True)
        serializer = TopicSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request, format=None):
        data = request.data
        if data:
            for item in data:
                try:
                    blog = Blog.objects.get(id=item)
                    if blog:
                        blog.delete()
                except:
                    return Response({"error": "Có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)
            return Response({"success": "Xóa blog thành công"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Đã có lỗi xảy ra"},status=status.HTTP_400_BAD_REQUEST)
