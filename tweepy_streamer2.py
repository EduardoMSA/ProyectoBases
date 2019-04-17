from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials

####CLIENTE###
class TwitterClient():

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().Authenticate_Twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

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

if __name__ == "__main__":

    hash_tag_list = ["Atlas","Seleccion","Chivas"]
    fetched_tweets_filename = "tweets.json"

    twitter_client = TwitterClient('pycon')
    lista = twitter_client.getFriendList(5)
    for i in lista:
        print(i)
        print()

    #twitterStreamer = TwitterStreamer()
    #twitterStreamer.stream_tweets(fetched_tweets_filename,hash_tag_list)
