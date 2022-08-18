from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Sitting, Winner, Wordle, Word
from words.telegram.bot import post_new_winner_on_telegram, post_published_quiz_on_telegram

@receiver(post_save, sender=Sitting)
def create_winner_from_sitting(sender, instance, created, **kwargs):
    if created and instance.can_create_winner():
        winner = Winner.objects.create(sitting=instance)
        found_word = Word.objects.get(pk=instance.word.id)
        found_word.found = True
        found_word.save()
        post_new_winner_on_telegram(winner)

@receiver(post_save, sender=Wordle)
def wordle_published_alert(sender, instance, created, **kwargs):
    if created and instance.status == 0:
        post_published_quiz_on_telegram(instance)

@receiver(post_save, sender=Winner)
def wordle_game_ended(sender, instance, created, **kwargs):
    number_of_winners_created = Winner.objects.filter(sitting__word__wordle__id=instance.sitting.word.wordle.id).count()
    if created and instance.sitting.word.wordle.no_of_words == number_of_winners_created:
        wordle = Wordle.objects.get(pk=instance.sitting.word.wordle.id)
        wordle.status = Wordle.ENDED
        wordle.save()
