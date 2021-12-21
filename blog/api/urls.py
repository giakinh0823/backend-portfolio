from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

router = routers.DefaultRouter()
router.register(r'blogs', views.BlogViewSet, basename='admin_blogs')
router.register(r'topics', views.TopicViewSet, basename='admin_topics')
router.register(r'tags', views.TagViewSet, basename='admin_tags')
router.register(r'photos', views.PhotoViewSet, basename='admin_photos')


urlpatterns = [
    
    #Photo
    path('admin/upload/', views.PhotoUpload.as_view(), name='photo_upload'),
    path('admin/upload/remove/', views.PhotoRemove.as_view(), name='photo_upload_remove'),
    path('admin/upload/<int:pk>/', views.PhotoUploadDetail.as_view(), name='photo_upload_detail'),
    
    #Blog
    path('admin/blog/<slug:slug>/', views.BlogDetailViewSet.as_view(), name='blog_slug'),
    path('admin/getBlogs/', views.BlogPublicViewSet.as_view(), name='blogs_admin'),
    path('admin/blogs/remove/', views.BlogRemoveAllViewSet.as_view(), name='blog_remove'),
    path('blogs/', views.BlogPublicViewSet.as_view(), name='blogs'),
    
    #Topic
    path('admin/topic/<slug:slug>/', views.TopicDetailViewSet.as_view(), name='topic_slug'),
    path('admin/topics/remove/', views.TopicRemoveAllViewSet.as_view(), name='topic_remove'),
    path('admin/topics/remove/<int:pk>/', views.TopicRemoveViewSet.as_view(), name='topic_remove_slug'),
    path('topics/', views.TopicPublicViewSet.as_view(), name='topics'),
    
    #tag
    path('admin/tags/remove/', views.TagRemoveAllViewSet.as_view(), name='tag_remove'),
    
    #admin
    path('admin/', include(router.urls)),
]
