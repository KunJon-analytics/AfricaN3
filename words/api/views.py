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
from words.models import Sitting, Winner, Wordle, Word

from .serializers import SittingSerializer, WordleSerializer, WordSerializer
from users.api.mixins import UserQuerySetMixin


class WordTodayView(APIView):
    """
    Gets a word that is not yet found from the active Wordle Game.

    * Requires user to be authenticated.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Returns the word for the day.
        * Requires user to be authenticated.
        * Can only be called once daily by a user
        """
        try:
            active_wordle_game = Wordle.objects.public().earliest()
            data = WordleSerializer(active_wordle_game).data

            return Response(data, status=status.HTTP_202_ACCEPTED)
        except Wordle.DoesNotExist:
            bad_content = {'detail': 'There is no active Wordle game right now'}

            return Response(bad_content, status=status.HTTP_204_NO_CONTENT)

class CreateSitting(APIView):
    """
    Submits a sitting to be stored and sends a signal
    to create winner

    * Requires user to be authenticated.
    * Can only be called once daily by a user
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        wordle = request.data.get("wordle")
        passed = request.data.get("passed")
        word_guessed = request.data.get("word_guessed") 
        data = {'user': user, 'wordle': wordle, 'passed': passed, 'word_guessed': word_guessed}
        serializer = SittingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)