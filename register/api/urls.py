
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .views import MyTokenObtainPairAdminView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'groups', views.GroupViewSet, basename='groups')

urlpatterns = [
    path('', include(router.urls)),
    path('token/admin/', MyTokenObtainPairAdminView.as_view(), name='token_obtain_pair_admin'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
