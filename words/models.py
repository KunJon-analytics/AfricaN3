from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone


class WordleManager(models.Manager):
    def public(self):
        now = timezone.now()
        return self.get_queryset().filter(status__lt=Wordle.ENDED, pub_date__lte=now)

class Wordle(models.Model):

    CREATED = 0
    ENDED = 1
    PAID = 2
    STATUS_CHOICES = (
        (CREATED, _('Created')),
        (ENDED, _('Ended')),
        (PAID, _('Paid')),
    )

    title = models.CharField(
        verbose_name=_("Title"), unique=True,
        max_length=60, blank=False)

    description = models.TextField(
        verbose_name=_("Description"),
        blank=True, help_text=_("a description of the wordle"))

    master = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='wordles', on_delete=models.CASCADE)

    status = models.PositiveSmallIntegerField(_("Status"), choices=STATUS_CHOICES, default=CREATED)

    reward = models.PositiveIntegerField(
        blank=True, null=True, verbose_name=_("Reward"),
        help_text=_("Total reward to be shared among winners"))

    created_date = models.DateField('date created', auto_now_add=True)

    pub_date = models.DateTimeField('date to be published', default=timezone.now)

    no_of_words = models.PositiveIntegerField(
        default=1, verbose_name=_("Max Words"),
        help_text=_("Number of words to be attempted for this game."),
        validators=[MaxValueValidator(7), MinValueValidator(1)])

    wordle_id = models.PositiveIntegerField(unique=True, verbose_name=_("Trivia ID"),
        help_text=_("Wordle identifier on the blockchain"))
    
    transaction_id = models.CharField(
        verbose_name=_("Transaction ID"), max_length=70, unique=True)

    objects = WordleManager()

    class Meta:
        verbose_name = _("Wordle")
        verbose_name_plural = _("Wordles")
        ordering = ['pub_date', 'title']
        get_latest_by = 'pub_date'

    def __str__(self):
        return self.title

    def is_public(self):
        if self.pub_date is None:
            return False
        if self.status == 0:
            return False
        now = timezone.now()
        is_in_past = now >= self.pub_date
        return is_in_past

    def single_winner_reward(self):
        amount = self.reward / self.no_of_words
        return amount


class Letter(models.Model):
    """
    Used to store english letters.

    """
    key = models.CharField(max_length=1, unique=True,
                               blank=False,
                               help_text=_("Enter the letter that "
                                           "you want displayed"),
                               verbose_name=_("Key"))

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = _("Letter")
        verbose_name_plural = _("Letters")

class Word(models.Model):
    """
    Used to store the words for a wordle game.

    """
    content = models.CharField(max_length=5,
                               blank=False,
                               help_text=_("Enter the word text that "
                                           "you want displayed"),
                               verbose_name=_("Content"))

    found = models.BooleanField(default=False, blank=False,
                                   verbose_name=_("Found"))

    wordle = models.ForeignKey(Wordle, related_name='words',
                             verbose_name=_("Wordle"), on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = _("Word")
        verbose_name_plural = _("Words")

class Sitting(models.Model):
    """
    Used to store the results of enrolled wordle takers.

    Created when the user shows interest/starts the wordle
    Can only be created every 12 hours

    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sittings',
                             verbose_name=_("User"), on_delete=models.CASCADE)

    word = models.ForeignKey(Word, related_name='sittings',
                             verbose_name=_("Word"), on_delete=models.CASCADE)

    attempts = models.PositiveIntegerField(
        default=1, verbose_name=_("Max Words"),
        help_text=_("Number of words to be attempted for this game."),
        validators=[MaxValueValidator(6), MinValueValidator(1)])

    word_guessed = models.CharField(max_length=5,
                               blank=False,
                               help_text=_("The 6th entry or the correct "
                                           "word if user guessed right"),
                               verbose_name=_("Content"))

    passed = models.BooleanField(default=False, blank=False,
                                   verbose_name=_("Passed"))

    end = models.DateTimeField(null=True, blank=True, verbose_name=_("End"), auto_now_add=True)

    class Meta:
        ordering = ['end']
        get_latest_by = 'end'

    def __str__(self):
        return "{} on {}" .format(self.user, self.wordle.title)


    def can_create_winner(self):
        """
        Finds if a winner instance can be created from
        a sitting instance created
        """
        found = self.word.found
        create_winner = False
        if found:
            create_winner = True
        return create_winner


class Winner(models.Model):
    sitting = models.OneToOneField(Sitting, on_delete=models.SET_NULL, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    claimed = models.BooleanField(default=False)

    def __str__(self):
        return "{} on {}" .format(self.sitting.user, self.sitting.wordle.title)
