# handling data
import pandas as pd
import numpy as np

# for network creation
import networkx as nx

pd.set_option('display.float_format', lambda x: '%.f' % x)

# Read json into a pandas dataframe
tweets_df = pd.read_json("tweets.txt", lines=True)

# Check the name of the columns
print(tweets_df.columns)

# Create a second dataframe to put important information
tweets_final = pd.DataFrame(
    columns=["createdAt", "id", "inReplyToScreenName", "inReplyToStatusId", "inReplyToUserId",
             "retweetedId", "retweetedScreenName", "userMentionsScreenName", "userMentionsId",
             "text", "userId", "screenName", "followersCount"])

# Columns that are going to be the same
equal_columns = ["created_at", "id", "text"]
tweets_final[equal_columns] = tweets_df[equal_columns]


# Get the basic information about user
def get_basics(tweets_final):
    tweets_final["screenName"] = tweets_df["user"].apply(lambda x: x["screen_name"])
    tweets_final["userId"] = tweets_df["user"].apply(lambda x: x["id"])
    tweets_final["followersCount"] = tweets_df["user"].apply(lambda x: x["followers_count"])
    return tweets_final


# Get the user mentions
def get_usermentions(tweets_final):
    # Inside the tag 'entities' will find 'user mentions' and will get 'screen name' and 'id'
    tweets_final["userMentionsScreenName"] = tweets_df["entities"].apply(
        lambda x: x["user_mentions"][0]["screen_name"] if x["user_mentions"] else np.nan)
    tweets_final["userMentionsId"] = tweets_df["entities"].apply(
        lambda x: x["user_mentions"][0]["id_str"] if x["user_mentions"] else np.nan)
    return tweets_final


# Get retweets
def get_retweets(tweets_final):
    # Inside the tag 'retweeted_status' will find 'user' and will get 'screen name' and 'id'
    tweets_final["retweetedScreenName"] = tweets_df["retweeted_status"].apply(
        lambda x: x["user"]["screen_name"] if x is not np.nan else np.nan)
    tweets_final["retweetedId"] = tweets_df["retweeted_status"].apply(
        lambda x: x["user"]["id_str"] if x is not np.nan else np.nan)
    return tweets_final


# Get the information about replies
def get_in_reply(tweets_final):
    # Just copy the 'in_reply' columns to the new dataframe
    tweets_final["inReplyToScreenName"] = tweets_df["in_reply_to_screen_name"]
    tweets_final["inReplyToStatusId"] = tweets_df["in_reply_to_status_id"]
    tweets_final["inReplyToUserId"] = tweets_df["in_reply_to_user_id"]
    return tweets_final


# Lastly fill the new dataframe with the important information
def fill_df(tweets_final):
    get_basics(tweets_final)
    get_usermentions(tweets_final)
    get_retweets(tweets_final)
    get_in_reply(tweets_final)
    return tweets_final


# Get the interactions between the different users
def get_interactions(row):
    # From every row of the original dataframe
    # First we obtain the 'userId' and 'screenName'
    user = row["userId"], row["screenName"]
    # Be careful if there is no user id
    if user[0] is None:
        return (None, None), []

    # The interactions are going to be a set of tuples
    interactions = set()

    # Add all interactions
    # First, we add the interactions corresponding to replies adding the id and screenName
    interactions.add((row["inReplyToUserId"], row["inReplyToScreenName"]))
    # After that, we add the interactions with retweets
    interactions.add((row["retweetedId"], row["retweetedScreenName"]))
    # And later, the interactions with user mentions
    interactions.add((row["userMentionsId"], row["userMentionsScreenName"]))

    # Discard if user id is in interactions
    interactions.discard((row["userId"], row["screenName"]))
    # Discard all not existing values
    interactions.discard((None, None))
    # Return user and interactions
    return user, interactions


tweets_final = fill_df(tweets_final)
tweets_final = tweets_final.where((pd.notnull(tweets_final)), None)
print(tweets_final.head(5))

graph = nx.Graph()
for index, tweet in tweets_final.iterrows():
    user, interactions = get_interactions(tweet)
    userId, user_name = user
    tweet_id = tweet["id"]
    for interaction in interactions:
        int_id, int_name = interaction
        graph.add_edge(userId, int_id, tweetId=tweet_id)

        graph.nodes[userId]["name"] = user_name
        graph.nodes[int_id]["name"] = int_name

nx.write_gml(graph, "graph.gml")
