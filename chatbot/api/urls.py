from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

router = routers.DefaultRouter()
router.register(r'messages', views.ChatbotMessageAdminViewSet, basename='admin_chatbot')
router.register(r'group_messages', views.ChatbotGroupAdminViewSet, basename='admin_chatbot')


urlpatterns = [
    # path('messages/', views.ChatbotsMessagePublicViewSet.as_view(), name='chatbots_message'),
    path('chatbots/join/', views.ChatbotGroupJoinViewSet.as_view(), name='chatbots_groups_join'),
    path('admin/chatbots/join/', views.ChatbotGroupJoinViewSet.as_view(), name='chatbots_groups_join'),
    path('chatbots/<str:id>/', views.ChatbotGroupDeatailPublicViewSet.as_view(), name='chatbots_groups_detail'),
    path('admin/chatbots/<str:id>/', views.ChatbotGroupDeatailPublicViewSet.as_view(), name='chatbots_groups_detail'),
    path('admin/chatbots/', views.ChatbotGroupAdminCustomViewSet.as_view(), name='chatbots_groups'),
    path('chatbots/', views.ChatbotGroupAdminCustomViewSet.as_view(), name='chatbots_groups'),
    path('admin/', include(router.urls)),
]
