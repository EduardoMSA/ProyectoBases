from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials

class TwitterStreamer():
    #Clase para streamind y procesamiento de tweets
    def stream_tweets(self,fetched_tweets_filename, hash_tag_list):
        # Esto maneja la autentufuación de twitter y la conección al API de Streaming fe Twitter.
        listener = StdOutListener(fetched_tweets_filename)
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY,twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN,twitter_credentials.ACCESS_TOKEN_SECRET)

        stream = Stream(auth, listener)

        stream.filter(track=hash_tag_list)

class StdOutListener(StreamListener):
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
        print(status)

if __name__ == "__main__":

    hash_tag_list = ["Atlas","Seleccion","Chivas"]
    fetched_tweets_filename = "tweets.json"

    twitterStreamer = TwitterStreamer()
    twitterStreamer.stream_tweets(fetched_tweets_filename,hash_tag_list)
