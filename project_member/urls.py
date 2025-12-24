from django.urls import path, include
from rest_framework.routers import DefaultRouter

from project_member.views import ProjectMemberViewSet


router = DefaultRouter()
router.register(r'', ProjectMemberViewSet, basename='project member')

urlpatterns = [
    path('', include(router.urls)),
]
