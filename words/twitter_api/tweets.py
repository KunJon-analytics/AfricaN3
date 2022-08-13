import os
import collections
import json
import re
import random

import tweepy as tw
import nltk
from nltk.corpus import stopwords
from words.models import Word, Wordle

from django.conf import settings

json_path = settings.BASE_DIR / 'words' / 'twitter_api' / 'data.json'

CONSUMERKEY = "sX6o9mxb4hNd3yGMOeJ2nWOIP"
CONSUMERSECRET = "LB1cyZSvjI9pGwwsT9FGeyTnJgMtTbrAUSrZuVQJnJbOZw20WD"
ACCESSTOKEN = "1205399139040804864-mi6xcU8e374XIqFZoo3fTtAB4uqy8n"
ACCESSTOKENSECRET = "xharzLg3XPfYQr58h0tnlEj1p5TeabVg7TGKR1NK2tegO"

auth = tw.OAuth1UserHandler(
   CONSUMERKEY, CONSUMERSECRET, ACCESSTOKEN, ACCESSTOKENSECRET
)
# auth = tweepy.OAuth1UserHandler(
#    settings.CONSUMERKEY, settings.CONSUMERSECRET, settings.ACCESSTOKEN, settings.ACCESSTOKENSECRET
# )

api = tw.API(auth)

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Opening JSON file
f = open(json_path)

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list
five_lettered_words = [entry for entry in data['words']]

# Closing file
f.close()


def remove_url(txt):
   """Replace URLs found in a text string with nothing 
   (i.e. it will remove the URL from the string).

   Parameters
   ----------
   txt : string
      A text string that you want to parse and remove urls.

   Returns
   -------
   The same txt string with url's removed.
   """

   return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())

def remove_words_with_number(txt):
   """Replace words with numbers found in a text string with nothing 
   (i.e. it will remove the word with numbers from the string).

   Parameters
   ----------
   txt : string
      A text string that you want to parse and remove words with numbers.

   Returns
   -------
   The same txt string with numbers removed.
   """
   return re.sub(r'\w*\d\w*', '', txt).strip()

# most common 5 words
def most_frequent(List, no_of_words):
   """Takes a list of words and returns the n most  
   common words.

   Parameters
   ----------
   List : list
      A list of strings.

   no_of_words : integer
      The number of words to be returned

   Returns
   -------
   A list of the n most popular words.
   """
   occurence_count = collections.Counter(List)
   return occurence_count.most_common(no_of_words)

def complete_wordle_words(List, no_of_words, wordle):
   """Takes a number and creates the n random words.
   It should exclude words already related to the wordle game

   get list of words
   use exclude to ensure they are not among

   Parameters
   ----------

   List : list
      A list of freq words tuple.

   no_of_words : integer
      The number of words to be returned

   wordle : Wordle
      The Wordle instance the word(s) are being
      generated for

   """
   
   words_to_exclude = [entry[0] for entry in List]

   qs = [entry for entry in five_lettered_words if entry not in words_to_exclude]
   random.shuffle(qs)
   for x in range(no_of_words):
      random_object = qs[x]
      Word.objects.create(content = random_object, wordle = wordle)


def create_wordle_words(wordle_pk, searchlight):
   """
    Creates the words for a wordle game

    * Requires the wordle pk and the search word.
    """
   tweets = tw.Cursor(api.search_tweets, searchlight,
                            count=100).items(1000)

   all_tweets = [tweet.text for tweet in tweets]
   all_tweets_no_urls = [remove_url(tweet) for tweet in all_tweets]
   all_tweets_no_numbers = [remove_words_with_number(tweet) for tweet in all_tweets_no_urls]

   # Create a list of lists containing lowercase words for each tweet
   words_in_tweet = [tweet.lower().split() for tweet in all_tweets_no_numbers]

   # Remove stop words
   tweets_nsw = [[word for word in tweet_words if not word in stop_words]
               for tweet_words in words_in_tweet]

   # Remove words that are not 5 lettered
   tweets_nsw_five = [[word for word in tweet_words if len(word) == 5]
               for tweet_words in tweets_nsw]

   # Remove empty List from List
   # using list comprehension
   res = [ele for ele in tweets_nsw_five if ele != []]

   # flatten list
   flat_list = [item for sublist in res for item in sublist]

   # Get Wordle
   wordle = Wordle.objects.get(pk = wordle_pk)
   words_needed = wordle.no_of_words

   freq_words = most_frequent(flat_list, words_needed)

   words_returned = len(freq_words)
   if words_returned == words_needed:
      for words in freq_words:
         Word.objects.create(content = words[0], wordle = wordle)
   else:
      number = words_needed - words_returned
      complete_wordle_words(freq_words, number, wordle)


create_wordle_words(1, "$TTM")