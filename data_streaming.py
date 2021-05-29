import tweepy

consumer_key = "ux4LqNxokmQHnM4QiGstZKdYs"
consumer_secret = "awr4nOz2q9TPw0qZAbhnpELN6VOba8g9xhSGRHqedqYJiLame5"
access_token = "1201552701445816322-Ok7EizZ0bWbpCGnauWXqEHEFYzGfLq"
access_token_secret = "KH7iywhezzETrdvrnGi0UC9ixMqiTMteTqVfXei3Lopge"

dbnametwitter = "testpython"
usertwitter = "ioana"
passwordtwitter = "ioana"
hosttwitter = "localhost"
porttwitter = "5432"


# Accesing twitter from the App created in my account
def autorize_twitter_api():
    """
    This function gets the consumer key, consumer secret key, access token
    and access token secret given by the app created in your Twitter account
    and authenticate them with Tweepy.
    """
    # Get access and costumer key and tokens
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return auth


class MyStreamListener(tweepy.StreamListener):
    """
    def on_status(self, status):
        print(status.text)
    """

    def __init__(self, filename, api=None):
        self.filename = filename

        tweepy.StreamListener.__init__(self, api=api)

    def on_data(self, raw_data):

        try:
            with open(self.filename, 'a') as file:
                file.write(raw_data)

        except Exception as e:
            print(e)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False


# For realtime streaming
if __name__ == "__main__":
    # Creates the table for storing the tweets
    term_to_search = "avengers"

    # Connect to the streaming twitter API
    api = tweepy.API(wait_on_rate_limit_notify=True)

    # Stream the tweets
    streamer = tweepy.Stream(auth=autorize_twitter_api(), listener=MyStreamListener(api=api, filename='tweets.txt'))
    streamer.filter(languages=["en"], track=[term_to_search])
