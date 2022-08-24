from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.generics import ListAPIView

from words.models import Wordle, Letter, Winner
from words.twitter_api.tweets import create_wordle_words
from words.telegram.bot import post_rewards_sent_on_telegram
from .mixins import UserQuerySetMixin
from .serializers import SittingSerializer, WordleSerializer, AddWordleSerializer, LetterSerializer, WinnerSerializer, WordleSittingsSerializer


class LetterList(ListAPIView):
    queryset = Letter.objects.all()
    serializer_class = LetterSerializer
    permission_classes = [IsAuthenticated]

class WordTodayView(APIView):
    """
    Gets a word that is not yet found from the active Wordle Game.

    * Requires user to be authenticated.
    """
    permission_classes = [IsAuthenticated]
    throttle_scope = 'game'

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
    to create winner / end game / 

    * Requires user to be authenticated.
    * Can only be called once daily by a user
    """
    permission_classes = [IsAuthenticated]
    throttle_scope = 'game'

    def post(self, request):
        user = request.user.id
        word = request.data.get("word")
        passed = request.data.get("passed")
        word_guessed = request.data.get("word_guessed") 
        attempts = request.data.get("attempts") 
        data = {'user': user, 'word': word, 'passed': passed, 'word_guessed': word_guessed, 'attempts': attempts}
        serializer = SittingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateWordle(APIView):
    """
    Creates a new wordle game

    * Requires user to be authenticated.
    * tx_id must be confirmed to ensure payment is made
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        # words_added = data.pop("words_added")
        searchlight = data.pop("search_twitter")
        # if words_added:
        #     serializer = WordleSerializer(data=data)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        #     else:
        #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # else:
        serializer = AddWordleSerializer(data=data)
        if serializer.is_valid():
            wordle = serializer.save()
            create_wordle_words(wordle.pk, searchlight)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WinningListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WinnerSerializer

    def get_queryset(self):
        """
        This view should return a list of all the unclaimed winnings
        for the currently authenticated user.
        """
        user = self.request.user
        return Winner.objects.filter(sitting__user=user, sitting__word__wordle__status=Wordle.PAID, claimed=False)

class MasterListView(UserQuerySetMixin, ListAPIView):
    user_field = 'master'
    permission_classes = [IsAuthenticated]
    serializer_class = WordleSittingsSerializer

    def get_queryset(self):
        """
        This view should return a list of all the games created by the
        currently authenticated user / admin that have ended and have not being paid.
        """
        return Wordle.objects.filter(status=Wordle.ENDED)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def winners_publish_view(request, *args, **kwargs): 
    data = request.data
    transaction_id = data.get("transaction_id")
    wordle_id = data.get("wordle_id")
    obj = get_object_or_404(Wordle, pk=wordle_id)
    is_admin = request.user.is_staff
    allowed = is_admin

    if len(transaction_id) > 0 and allowed and obj.status == Wordle.ENDED:
        # todo: check for validity of the transaction_id

        # create a payment instance, publish quiz and send TG message
        obj.status = Wordle.PAID
        obj.save()
        winners = Winner.objects.filter(sitting__word__wordle=obj)
        post_rewards_sent_on_telegram(winners, obj)
        content = {'detail': 'The wordle winners have been successfully published'}
        return Response(content, status=status.HTTP_202_ACCEPTED)
    bad_content = {'detail': 'Invalid request sent'}
    return Response(bad_content, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def winner_claim_view(request, *args, **kwargs): 
#     data = request.data
#     transaction_id = data.get("transaction_id")
#     wordle_id = data.get("wordle_id")
#     obj = get_object_or_404(Wordle, pk=wordle_id)

#     if len(transaction_id) > 0 and obj.status == Wordle.PAID:
#         # todo: check for validity of the transaction_id

#         # get the winner instance and set claimed to true
#         try:
#             winner_instance = Winner.objects.get(Q(sitting__word__wordle=obj),Q(sitting__user=request.user))
#         except Winner.DoesNotExist:
#             raise Http404
#         except Winner.MultipleObjectsReturned:
#             winner_instance = Winner.objects.filter(sitting__word__wordle=obj, sitting__user=request.user).first()
#         winner_instance.claimed = True
#         winner_instance.save()
#         content = {'detail': 'Reward claimed successfully'}
#         return Response(content, status=status.HTTP_202_ACCEPTED)
#     bad_content = {'detail': 'Invalid request sent'}
#     return Response(bad_content, status=status.HTTP_400_BAD_REQUEST)