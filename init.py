from time import sleep
import tweepy
import praw
import datetime

from config import config
from keys import keys

subreddit = config['subreddit']
get_data = dict()
timestamp = 60 * 60 * config['hours']

# REST API connection
reddit = praw.Reddit(client_id=keys['reddit_client_id'],
                     client_secret=keys['reddit_client_secret'],
                     user_agent=keys['reddit_user_agent'],
                     username=keys['reddit_username'],
                     password=keys['reddit_password'])

while True:
    submissions = reddit.subreddit(subreddit).new(limit=100)
    for submission in submissions:
        if submission.url in get_data:
            if submission.created > get_data[submission.url]:
                if submission.created - timestamp < get_data[submission.url]:
                    print(submission.url + " already posted")
                    submission.reply(
                        "This link was already posted in the last 24h.")

                    submission.mod.flair("Repost - Removed")
                    submission.mod.remove()
                else:
                    del get_data[submission.url]
                    print(submission.url + " removed from blocked urls.")

        get_data[submission.url] = submission.created
        datetime.datetime.fromtimestamp(submission.created)
    sleep(10)
