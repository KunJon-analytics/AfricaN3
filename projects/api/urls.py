from django.urls import path

from .views import (
    ProjectList,
)

app_name = 'projects'

urlpatterns = [
    path('', ProjectList.as_view()),
]