from django.conf import settings

import tweepy

CONSUMERKEY = "sX6o9mxb4hNd3yGMOeJ2nWOIP"
CONSUMERSECRET = "LB1cyZSvjI9pGwwsT9FGeyTnJgMtTbrAUSrZuVQJnJbOZw20WD"
ACCESSTOKEN = "1205399139040804864-mi6xcU8e374XIqFZoo3fTtAB4uqy8n"
ACCESSTOKENSECRET = "xharzLg3XPfYQr58h0tnlEj1p5TeabVg7TGKR1NK2tegO"

auth = tweepy.OAuth1UserHandler(
   CONSUMERKEY, CONSUMERSECRET, ACCESSTOKEN, ACCESSTOKENSECRET
)
# auth = tweepy.OAuth1UserHandler(
#    settings.CONSUMERKEY, settings.CONSUMERSECRET, settings.ACCESSTOKEN, settings.ACCESSTOKENSECRET
# )

api = tweepy.API(auth)
number = 0

for status in tweepy.Cursor(api.search_tweets, "$nudes",
                            count=100).items(250):
    print(status.text)
    number = number + 1
    print(number)