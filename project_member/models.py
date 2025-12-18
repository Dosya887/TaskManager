from django.db import models

from project.models import Project
from project_member.choices import ProjectRole
from user.models import User


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_members')
    role = models.CharField(max_length=33, choices=ProjectRole.choices,
                            default=ProjectRole.MEMBER)

    def __str__(self):
        return f'{self.user} → {self.project} ({self.role})'

    class Meta:
        unique_together = ('project', 'user')
