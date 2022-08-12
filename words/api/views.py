from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q

from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from words.models import Sitting, Winner, Wordle

from .serializers import WordleSerializer, WordSerializer
from users.api.mixins import UserQuerySetMixin


@api_view(['GET'])
def today_word_view(request):
    return Response({"message": "Hello for today! See you tomorrow!"})

class WordTodayView(APIView):
    """
    Gets a word that is not yet found from the active Wordle Game.

    * Requires user to be authenticated.
    """
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Returns the word for the day.
        """
        # Use try catch block here
        try:
            active_wordle_game = Wordle.objects.public().earliest()
            data = WordleSerializer(active_wordle_game).data

            return Response(data, status=status.HTTP_202_ACCEPTED)
        except Wordle.DoesNotExist:
            bad_content = {'detail': 'There is no active Wordle game right now'}

            return Response(bad_content, status=status.HTTP_204_NO_CONTENT)