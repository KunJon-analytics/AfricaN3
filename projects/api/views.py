from rest_framework import permissions
from rest_framework.generics import ListAPIView

from .serializers import ProjectSerializer
from ..models import Project


class ProjectList(ListAPIView):
    queryset = Project.objects.all().order_by('-id')[:6]
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]