"""Retrieve Tweets, word embedding, and populated DB """

import tweepy
import spacy
from .models import DB, Tweet, User
from os import getenv

# Grabbing Passwords from my .env file
TWITTER_API_KEY = getenv('TWITTER_API_KEY') 
TWITTER_API_KEY_SECRET = getenv('TWITTER_API_KEY_SECRET')
TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY,TWITTER_API_KEY_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)

# for turning our tweets into an array of numbers
nlp = spacy.load('my_model')
def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector


def add_or_update_user(username):
    try:
        """Allows us to add/update to our DB """
        twitter_user = TWITTER.get_user(username)
        # either updates or adds a user depending upon if they are in DB
        db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id, name=username)
        DB.session.add(db_user)

        tweets = twitter_user.timeline(
            count = 200, exclude_replies=True,
            includes_rts=False, tweet_mode = 'extended'
        )
   # will update the most recent tweet id to the user
    
        if tweets:
          db_user.newest_tweet_id = tweets[0].id


        for tweet in tweets:
             vectorized_tweet = vectorize_tweet(tweet.full_text)
             db_tweet = Tweet(
                 id=tweet.id, text=tweet.full_text,
                 vect=vectorized_tweet
             )
             db_user.tweets.append(db_tweet)
             DB.session.add(db_tweet)

    except Exception as e:
        print('Error Processing {}: {}'.format(username, e)) # gives an error
        raise e

  # last thing done is committing changes
    else: 
         DB.session.commit()

def update_all_users():
    """ Updates all tweets for all Users in User Table"""
    for user in User.query.all():
        add_or_update_user(user.name)

#def insert_example_users():
  # using our functions to add two users
 # add_or_update_user('elonmusk')
  #add_or_update_user('jackblack')