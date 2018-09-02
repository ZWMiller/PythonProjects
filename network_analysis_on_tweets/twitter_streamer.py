import os
from twitter_credentials import twit_auth as credentials
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
import json


auth = tweepy.OAuthHandler(credentials["consumer_key"],
                           credentials["consumer_secret"])
auth.set_access_token(credentials["access_token"],
                      credentials["access_token_secret"])

api=tweepy.API(auth)


class retweet_user_name_streamer(StreamListener):
    """
    Extension on Tweepy twitter streamer that stores retweet
    information about users and their connections to one another
    """

    def __init__(self, tweets_per_file=500, sep=";,."):
        """
        Twitter streamer that finds retweets and stores the username of both
        the retweeter and the original tweeter in a CSV file. Handles file
        management so the data is split across multiple CSV files.

        tweets_per_file: how many tweets to analyze and store per CSV
        sep: separator for CSV data, defaults to characters unlikely to be
        together in a twitter username
        """
        super().__init__()
        self.tweets_seen = 0
        self.current_file = 0
        self.tweets_per_file = tweets_per_file
        self.sep = sep
        self.base_file_name = "data/twitter_retweet_network_data{}.csv"
        self.file_to_write = None
        self.open_next_file()

    def open_next_file(self):
        """
        On call, opens a new file to be used in output and closes any open file.
        Manages the filename by making sure never to overwrite a previously created file.
        Sets the open file as an attribute for usage across the class.

        return: None
        """
        if self.file_to_write:
            self.file_to_write.close()

        file_name = self.get_valid_file_name()
        print("Opening File " + str(self.current_file))
        self.current_file += 1
        self.file_to_write = open(file_name, 'w')

    def get_valid_file_name(self):
        """
        File name selector helper function. Checks for existing files and
        iterates filenames until a valid, unused file name is found in the
        base filename directory.

        return: string, valid filename for data storage
        """
        file_name = self.base_file_name.format(self.current_file)
        if os.path.exists(file_name):
            while os.path.exists(file_name):
                self.current_file += 1
                file_name = self.base_file_name.format(self.current_file)
        return file_name


    def on_data(self, data):
        """
        When receiving data from the stream, check to see if it is a retweet (label RT),
        if it is, extract the username and check to see if the original tweet information
        is available. If so, store the usernames for the original tweeter and the retweeter
        so we can build a network graph. Also manages how many tweets are currently stored in
        each file.

        data: JSON object from twitter API stream
        return: None
        """
        tweet = json.loads(data)
        try:
            if tweet['text'].startswith('RT'):
                try:
                    user_original = tweet['user']['name']
                    self.file_to_write.write(user_original + self.sep + tweet['retweeted_status']['user']['name']+'\n')
                    self.tweets_seen += 1
                    if self.tweets_seen > self.tweets_per_file:
                        self.open_next_file()
                        self.tweets_seen = 0
                except KeyError:
                    pass
        except KeyError:
            pass

    def on_error(self, status):
        """
        If error from API, print the error.

        status: Error information
        return: None
        """
        print(status)

if __name__ == "__main__":
    twitter_stream = Stream(auth, retweet_user_name_streamer())
    twitter_stream.filter(track=['Trump', 'trump'])