from django.urls import path

from .views import (
    WordTodayView,
)


urlpatterns = [
    path('', WordTodayView.as_view()),
]
