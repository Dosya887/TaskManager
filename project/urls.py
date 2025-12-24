from django.urls import path
from rest_framework.routers import DefaultRouter

from project.views import ProjectViewSet


router = DefaultRouter()
router.register(r'project', ProjectViewSet, basename='project')

urlpatterns = [
    path('', ProjectViewSet.as_view(router.urls)),
]
