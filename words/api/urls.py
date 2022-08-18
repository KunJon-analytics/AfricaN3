from django.urls import path

from .views import (
    WordTodayView,
    CreateSitting,
    LetterList,
    CreateWordle,
    WinningListView,
)

app_name = 'words'

urlpatterns = [
    path('', WordTodayView.as_view()),
    path('letters/', LetterList.as_view()),
    path('submit/', CreateSitting.as_view()),
    path('create/', CreateWordle.as_view()),
    path('wins/', WinningListView.as_view()),
]
