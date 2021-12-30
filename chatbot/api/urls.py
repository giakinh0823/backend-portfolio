from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

router = routers.DefaultRouter()
router.register(r'messages', views.ChatbotMessageAdminViewSet, basename='admin_chatbot')
router.register(r'group_messages', views.ChatbotGroupAdminViewSet, basename='admin_chatbot')


urlpatterns = [
    path('messages/', views.ChatbotsMessagePublicViewSet.as_view(), name='chatbots_message'),
    path('groups/', views.ChatbotGroupPublicViewSet.as_view(), name='chatbots_groups'),
    path('admin/', include(router.urls)),
]
