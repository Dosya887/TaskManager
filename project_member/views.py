from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from project_member.models import ProjectMember
from project_member.permissions import IsProjectOwnerOrManager
from project_member.serializers import ProjectMemberSerializer


class ProjectMemberViewSet(ModelViewSet):
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsAuthenticated, IsProjectOwnerOrManager]

    def get_queryset(self):
        return ProjectMember.objects.filter(project__member__user=self.request.user)
