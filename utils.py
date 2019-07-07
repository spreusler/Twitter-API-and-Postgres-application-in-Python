import config
import pandas as pd
from sqlalchemy import create_engine
import threading
import datetime
import tweepy


class Keyword:
    """Class for keyword object instantiation"""
    def __init__(self, keyword, wait_seconds):
        self.wait_seconds = wait_seconds
        self.keyword = keyword

    def insert_database(self):
        """Function to create a API query and database entry"""
        # Variable to count succesful inserts into database
        success = 0

        # Create database connection
        connection = config.db_dialect + '+' + config.db_driver + '://' \
                     + config.db_username + ':' + config.db_password \
                     + '@' + config.db_database + '.' + config.db_address\
                     + ':' + config.db_port + '/' + config.db_database
        engine = create_engine(connection)

        # Connect to Twitter API
        api = twitter()
        public_tweets = api.search(self.keyword)

        # Loop over extracted Tweets
        for tweet in public_tweets:
            # Get API values
            user_id = tweet.user.id_str
            user_name = tweet.user.name
            tweet_id = tweet.id_str
            text = tweet.text
            time = tweet.created_at
            location = tweet.user.location
            follower_count = tweet.user.followers_count
            friends_count = tweet.user.friends_count

            try:
                # Create Dataframe from entries
                df = pd.DataFrame()
                df = df.append({'tweet_id': tweet_id, 'user_id': user_id, 'user_name': user_name, 'text': text, 'time': time,
                                'location': location, 'follower_count': follower_count, 'tweet_keyword': self.keyword,
                                'friends_count': friends_count}, ignore_index=True)

                # Commit do database
                df.to_sql(config.db_table, engine, if_exists='append', index=False)

                # Count 'try' as success
                success += 1
            except:
                pass
            finally:
                # Closes database connection
                engine.dispose()

        # Loop for request optimization
        if success > 11:
            self.wait_seconds = self.wait_seconds - 5
        elif success < 5:
            self.wait_seconds = self.wait_seconds + 5
        else:
            pass

        # Get Timestamp
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print("API run completed for {0:}. Success Rate: {1:.0%}. Time: {2:}"
              .format(self.keyword, success / 15, timestamp))
        threading.Timer(self.wait_seconds, self.insert_database).start()


class EntryAlreadyExists(Exception):
    """Exception Class if a database entry already exists"""
    pass


def twitter():
    """Twitter authentification function"""
    # Authentification
    consumer_key = config.consumer_key
    consumer_secret = config.consumer_secret

    # Twitter app access data
    access_token = config.access_token
    access_token_secret = config.access_token_secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    return api


# Function to create objects
def create_object_list():
    """Function to create a list of twitter keyword objects"""
    objs = list()
    for tweet_keyword in config.TWEET_KEYWORDS:
        obj = Keyword(tweet_keyword, config.START_TIMER)
        objs.append(obj)
    return objs
