import requests

import app_token
import tweepy

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import csv
import json


from datetime import date, datetime
import uuid

client = tweepy.Client(app_token.ACCESS_TOKEN)

input = input("What should our query be? ")
res = client.search_recent_tweets(f"{input} -is:retweet", max_results=30)

tweets = []

analyzer = SentimentIntensityAnalyzer()

for item in res.data:

    text = item.text
    vs = analyzer.polarity_scores(text)
    tweet_obj = {}
    try:
        tweet_obj['tweet'] = u"{}".format(text)
        tweet_obj['neg'] = vs['neg']
        tweet_obj['neu'] = vs['neu']
        tweet_obj['pos'] = vs['pos']
        tweet_obj['compound'] = vs['compound']
        tweets.append(tweet_obj)
    except:
        print("Failed to write row.")

tweets = sorted(tweets, key=lambda d: -d['compound'])

for tweet in tweets:
    try:
        print(tweet)
    except:
        print("Couldn't print item")


date = date.today()
now = datetime.now().strftime("%H%M%S")
nonce = uuid.uuid4().hex[:3]
title = f"{input}-{date}-{now}-{nonce}"

with open(f"output/{title}.json", "w+") as f:
    json.dump(tweets, f, indent=6)

with open(f"output/{title}.csv", "w+", encoding="utf-8", newline="") as f:

    writer = csv.writer(f)

    writer.writerow(['tweet', 'negative',
                    'neutral', 'positive', 'compound'])

    for tweet in tweets:
        try:
            writer.writerow([tweet['tweet'], tweet['pos'],
                            tweet['neu'], tweet['neg'], tweet['compound']])
        except Exception as e:
            print(e)
