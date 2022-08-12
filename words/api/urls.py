from django.urls import path

from .views import (
    WordTodayView,
    CreateSitting,
)


urlpatterns = [
    path('', WordTodayView.as_view()),
    path('submit/', CreateSitting.as_view()),
]
