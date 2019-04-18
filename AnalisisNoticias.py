from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials
import numpy as np
import pandas as pd

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

class TwitterAuthenticator():
    def Authenticate_Twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY,twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN,twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

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

    file = open("fuentes.csv","r")
    if file.mode == "r":
        content = file.read()
        fuentes = content.split(",")

    twitterclient = TwitterClient()
    tweet_analyser = TweetAnalyser()
    api = twitterclient.getTwitterClientAPI()

    for fuente in fuentes:
        print(fuente)
        try:
            tweets = api.user_timeline(screen_name=fuente, count = 100)
            df = tweet_analyser.tweets_to_data_frame(tweets)
            archivo = "Datos/" + fuente + ".csv"
            df.to_csv(archivo ,sep='\t',encoding='utf-8', index=False)
        except tweepy.TweepError:
            print("La cuenta -> " + fuente + " está protegida, saltando cuenta...")





    #print(tweets[0].id)
    #print(tweets[0].retweet_count)


    #df.to_json('ejemplo.json')
