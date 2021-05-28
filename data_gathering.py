import psycopg2
import tweepy
import json
import numpy as np

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


def create_tweets_table(term_to_search):
    """
    This function open a connection with an already created database and creates a new table to
    store tweets related to a subject specified by the user
    """

    # Connect to Twitter Database created in Postgres
    conn_twitter = psycopg2.connect(dbname=dbnametwitter, user=usertwitter, password=passwordtwitter, host=hosttwitter,
                                    port=porttwitter)

    # Create a cursor to perform database operations
    cursor_twitter = conn_twitter.cursor()

    # with the cursor now, create two tables, users twitter and the corresponding table according to the selected topic
    cursor_twitter.execute("CREATE TABLE IF NOT EXISTS twitter_users (user_id VARCHAR PRIMARY KEY, user_name VARCHAR);")

    query_create = "CREATE TABLE IF NOT EXISTS %s (id SERIAL, created_at timestamp, tweet text NOT NULL, " \
                   "user_id VARCHAR, user_name VARCHAR, retweetstatus_user int, retweetstatus_name VARCHAR, " \
                   "PRIMARY KEY(id), FOREIGN KEY(user_id) REFERENCES twitter_users(user_id));" % (
                           "tweets_predict_" + term_to_search)
    cursor_twitter.execute(query_create)

    # Commit changes
    conn_twitter.commit()

    # Close cursor and the connection
    cursor_twitter.close()
    conn_twitter.close()
    return


def store_tweets_in_table(term_to_search, created_at, tweet, user_id, user_name, retweetstatus_user,
                          retweetstatus_name):
    """
    This function open a connection with an already created database and inserts into corresponding table
    tweets related to the selected topic
    """

    # Connect to Twitter Database created in Postgres
    conn_twitter = psycopg2.connect(dbname=dbnametwitter, user=usertwitter, password=passwordtwitter, host=hosttwitter,
                                    port=porttwitter)

    # Create a cursor to perform database operations
    cursor_twitter = conn_twitter.cursor()

    # with the cursor now, insert tweet into table
    cursor_twitter.execute(
        "INSERT INTO twitter_users (user_id, user_name) VALUES (%s, %s) ON CONFLICT(user_id) DO NOTHING;",
        (user_id, user_name))

    cursor_twitter.execute(
        "INSERT INTO %s (created_at, tweet, user_id, user_name, retweetstatus_user, retweetstatus_name) VALUES (%%s, "
        "%%s, %%s, %%s, %%s, %%s);" % (
                'tweets_predict_' + term_to_search),
        (created_at, tweet, user_id, user_name, retweetstatus_user, retweetstatus_name))

    # Commit changes
    conn_twitter.commit()

    # Close cursor and the connection
    cursor_twitter.close()
    conn_twitter.close()
    return


class MyStreamListener(tweepy.StreamListener):
    """
    def on_status(self, status):
        print(status.text)
    """

    def on_data(self, raw_data):

        try:
            global term_to_search

            data = json.loads(raw_data)

            # Obtain all the variables to store in each column
            user_id = data['user']['id']
            user_name = data['user']['name']
            created_at = data['created_at']
            tweet = data['text']
            if data['retweeted_status']:
                retweetstatus_user = data['retweeted_status']['user']['id']
                retweetstatus_name = data['retweeted_status']['user']['name']
            else:
                retweetstatus_user = np.nan
                retweetstatus_name = ""

            # Store them in the corresponding table in the database
            store_tweets_in_table(term_to_search, created_at, tweet, user_id, user_name, retweetstatus_user,
                                  retweetstatus_name)

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
    create_tweets_table(term_to_search)

    # Connect to the streaming twitter API
    api = tweepy.API(wait_on_rate_limit_notify=True)

    # Stream the tweets
    streamer = tweepy.Stream(auth=autorize_twitter_api(), listener=MyStreamListener(api=api))
    streamer.filter(languages=["en"], track=[term_to_search])
