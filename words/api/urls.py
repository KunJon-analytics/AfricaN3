from django.urls import path

from .views import (
    WordTodayView,
    CreateSitting,
    LetterList,
    CreateWordle,
    WinningListView,
    MasterListView,
    winners_publish_view,
    # winner_claim_view,
)

app_name = 'words'

urlpatterns = [
    path('', WordTodayView.as_view()),
    path('letters/', LetterList.as_view()),
    path('submit/', CreateSitting.as_view()),
    path('create/', CreateWordle.as_view()),
    path('wins/', WinningListView.as_view()),
    path('unpaid/', MasterListView.as_view()),
    path('publish-winners/', winners_publish_view),
    # path('claim-reward/', winner_claim_view),
]
