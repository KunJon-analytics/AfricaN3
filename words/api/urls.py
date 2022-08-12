from django.urls import path

from .views import (
    WordTodayView,
    CreateSitting,
    CreateWordle,
)


urlpatterns = [
    path('', WordTodayView.as_view()),
    path('submit/', CreateSitting.as_view()),
    path('create/', CreateWordle.as_view()),
]
