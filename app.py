import tweepy
from flask import Flask
from concurrent.futures import ThreadPoolExecutor
from tweet_util import *

# Maximum of 2 thread workers
executor = ThreadPoolExecutor(2)

app = Flask(__name__)

# Authenticate Twitter account
auth = tweepy.OAuthHandler('ddnsdyRVRFLjPFsfbIV7kCgo0',
                           'UCv62xY76M0AMFULs9BFRGrhZuj4RM2wvkT9PwRpToqEOGkSYJ')

auth.set_access_token('1223203700040175616-rmVFV5k7P13QMwxwRlArta6agtmD2I',
                      'D25aILraVldNYeij3tQNk6Tyfgeh19a45ogq4COXHKKZD')

api = tweepy.API(auth)

tweet = ''


@app.route('/165NLjw4wWvWIqQUs3wyCwj1cYciQU')
def send_tweet():
    executor.submit(do_magic)

    return 'Sending Tweet'


@app.route('/get_last_tweet')
def get_last_tweet():

    return tweet


def do_magic():
    global tweet
    artist, song_name, lyrics = prepare_tweet_content()

    tweet = get_tweet_string(artist, song_name, lyrics)

    # Send the tweet
    api.update_status(tweet)


if __name__ == '__main__':
    app.run()
