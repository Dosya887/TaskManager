from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', include('user.urls')),
    path('api/v1/project/', include('project.urls')),
    # path('api/v1/project-member/', include('project_member.urls')),
    path('api/v1/tasks/', include('task.urls')),
    # path('api/v1/comment/', include('comment.urls')),
]
if settings.DEBUG:
    urlpatterns += [path('', include('core.swagger_urls'))]
