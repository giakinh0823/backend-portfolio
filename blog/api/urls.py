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
    path('admin/', include(router.urls)),
    path('admin/upload/', views.PhotoUpload.as_view(), name='photo_upload'),
    path('blogs/', views.BlogPublicViewSet.as_view(), name='blogs'),
    path('topics/', views.TopicPublicViewSet.as_view(), name='topics'),
]
