import os

from django.views import View
from django.http import HttpResponse, HttpResponseNotFound

from rest_framework import permissions
from rest_framework.generics import ListAPIView

from .serializers import ProjectSerializer
from ..models import Project


class ProjectList(ListAPIView):
    queryset = Project.objects.all().order_by('-id')[:6]
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]

class Assets(View):

    def get(self, _request, filename):
        path = os.path.join(os.path.dirname(__file__), 'static', filename)

        if os.path.isfile(path):
            with open(path, 'rb') as file:
                return HttpResponse(file.read(), content_type='application/javascript')
        else:
            return HttpResponseNotFound()