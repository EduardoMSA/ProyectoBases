from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials
import numpy as np
import pandas as pd


####CLIENTE###
class TwitterClient():

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().Authenticate_Twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def getTwitterClientAPI(self):
        return self.twitter_client

    def getUserTimelineTweets(self, numTweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id = self.twitter_user).items(numTweets):
            tweets.append(tweet)
        return tweets

    def getFriendList(self, numFriends):
        friends = []
        for friend in Cursor(self.twitter_client.friends, id = self.twitter_user).items(numFriends):
            friends.append(friend)
        return friends

    def getHomeTimeline(self, numTweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id = self.twitter_user).items(numTweets):
            tweets.append(tweet)
        return tweets


####AUTENTICADOR###
class TwitterAuthenticator():
    def Authenticate_Twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY,twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN,twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth


###STREAMER###
class TwitterStreamer():

    def __init__(self):
        self.twitterAuthenticator = TwitterAuthenticator()
    #Clase para streamind y procesamiento de tweets
    def stream_tweets(self,fetched_tweets_filename, hash_tag_list):
        # Esto maneja la autentufuación de twitter y la conección al API de Streaming fe Twitter.
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitterAuthenticator.Authenticate_Twitter_app()
        stream = Stream(auth, listener)
        stream.filter(track=hash_tag_list)


###LSITENER###
class TwitterListener(StreamListener):
    #Listener basico que solo imprime tweets.
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename=fetched_tweets_filename

    def on_data(self,data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
        except BaseException as e:
            print("Error on data: %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            #Regresa False en caso de que se esceda el limite del API
            print("ERROR 420")
            return False
        print(status)

class TweetAnalyser():
    #Analisis y categorizado de contenido de Tweets
    def tweets_to_data_frame(self,tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['rt'] = np.array([tweet.retweet_count for tweet in tweets])

        return df

if __name__ == "__main__":

    twitterclient = TwitterClient()
    tweet_analyser = TweetAnalyser()
    api = twitterclient.getTwitterClientAPI()

    tweets = api.user_timeline(screen_name="realDonaldTrump", count = 20)
    df = tweet_analyser.tweets_to_data_frame(tweets)
    #print(dir(tweets[0]))
    #print(tweets[0].id)
    #print(tweets[0].retweet_count)


    print(df.head(10))




    #twitterStreamer = TwitterStreamer()
    #twitterStreamer.stream_tweets(fetched_tweets_filename,hash_tag_list)
