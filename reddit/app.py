
import requests
import gen_token as gen_token

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import csv
import json

from datetime import date, datetime
import uuid


sub = input("Choose the subreddit: ")
# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'sent_analysis/0.0.1'}
TOKEN = gen_token.run()
print(TOKEN)

# add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

res = requests.get(f"https://oauth.reddit.com/r/{sub}/hot", headers=headers)
# let's see what we get

for post in res.json()['data']['children']:
    try:
        print(post['data']['title'])
    except:
        print("Couldn't print title")

analyzer = SentimentIntensityAnalyzer()

sentiment_list = []

for post in res.json()['data']['children']:

    post_obj = {}
    post_title = post['data']['title']
    vs = analyzer.polarity_scores(post_title)
    try:
        post_obj['title'] = post_title
        post_obj['neg'] = vs['neg']
        post_obj['neu'] = vs['neu']
        post_obj['pos'] = vs['pos']
        post_obj['compound'] = vs['compound']
        sentiment_list.append(post_obj)
    except:
        print("Failed to write row.")

sorted_sentiment_list = sorted(sentiment_list, key=lambda d: -d['compound'])

date = date.today()
now = datetime.now().strftime("%H%M%S")
nonce = uuid.uuid4().hex[:3]
title = f"{sub}-{date}-{now}-{nonce}"

with open(f"output/{title}.json", "w+") as f:
    json.dump(sorted_sentiment_list, f, indent=6)

with open(f"output/{title}.csv", "w+", encoding="utf-8", newline="") as f:

    writer = csv.writer(f)

    writer.writerow(['post_title', 'negative',
                    'neutral', 'positive', 'compound'])

    for item in sorted_sentiment_list:
        try:
            writer.writerow([item['title'], item['pos'],
                            item['neu'], item['neg'], item['compound']])
        except:
            print("Failed to write row.")
