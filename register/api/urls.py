
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .views import MyTokenObtainPairAdminView, UserFromTokenViewSet, UserPublicViewSet

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'groups', views.GroupViewSet, basename='groups')

urlpatterns = [
    path('admin/', include(router.urls)),
    path('token/', MyTokenObtainPairAdminView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/user/', UserFromTokenViewSet.as_view(), name='get_user_admin'),
    path('admin/token/', MyTokenObtainPairAdminView.as_view(), name='token_obtain_pair_admin'),
    path('admin/token/refresh/', TokenRefreshView.as_view(), name='token_refresh_admin'),
    path('users/', UserPublicViewSet.as_view(), name='get_user'),
]
