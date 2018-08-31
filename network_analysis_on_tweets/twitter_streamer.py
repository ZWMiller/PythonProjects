try:
    from requests_oauthlib import OAuth1
    import os
except ModuleNotFoundError:
    import sys
    import os

    # I need this because requests_oauth gets installed in a weird place on my system
    sys.path.append('/usr/local/lib/python3.6/site-packages')
    from requests_oauthlib import OAuth1

from twitter_credentials import twit_auth as credentials
import tweepy

auth = tweepy.OAuthHandler(credentials["consumer_key"],
                           credentials["consumer_secret"])
auth.set_access_token(credentials["access_token"],
                      credentials["access_token_secret"])

api=tweepy.API(auth)

from tweepy import Stream
from tweepy.streaming import StreamListener
from IPython import display
from collections import deque
import json


class MyListener(StreamListener):
    def __init__(self, tweets_per_file=500):
        super().__init__()
        self.tweets_seen = 0
        self.current_file = 0
        self.tweets_per_file = tweets_per_file
        self.file_to_write = None
        self.open_next_file()

    def open_next_file(self):
        if self.file_to_write:
            self.file_to_write.close()

        file_name = "data/twitter_retweet_network_data{}.csv".format(self.current_file)
        if os.path.exists(file_name):
            while os.path.exists(file_name):
                self.current_file += 1
                file_name = "data/twitter_retweet_network_data{}.csv".format(self.current_file)
        print("Opening File " + str(self.current_file))
        self.current_file += 1
        self.file_to_write = open(file_name, 'w')


    def on_data(self, data):
        tweet = json.loads(data)
        try:
            if tweet['text'].startswith('RT'):
                try:
                    user_original = tweet['user']['name']
                    self.file_to_write.write(user_original+';,.'+tweet['retweeted_status']['user']['name']+'\n')
                    self.tweets_seen += 1
                    if self.tweets_seen > self.tweets_per_file:
                        self.open_next_file()
                        self.tweets_seen = 0
                except KeyError:
                    pass
        except KeyError:
            pass

    def on_error(self, status):
        print(status)

if __name__ == "__main__":
    twitter_stream = Stream(auth, MyListener())
    twitter_stream.filter(track=['Trump', 'trump'])