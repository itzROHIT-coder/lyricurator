import tweepy
from flask import Flask
from concurrent.futures import ThreadPoolExecutor
from tweet_util import *

# Maximum of 2 thread workers
executor = ThreadPoolExecutor(2)

app = Flask(__name__)

# Authenticate Twitter account
auth = tweepy.OAuthHandler('UooCn40p2qSs3YRNXW54kliVt',
                           'l14v1E9vjvGT3tNamWqzxoH2ObWMcZaI7Uwpg1ZdY9k9urOD4R')

auth.set_access_token('1223203700040175616-5m0hCCA03wGaGQ6BvjlnAGcvpkk8rz',
                      '4Wau7gTnyzWG2rQ9TrgumbIxUDEAnWK85DbJnDR52Kf4D')

api = tweepy.API(auth)


@app.route('/165NLjw4wWvWIqQUs3wyCwj1cYciQU')
def send_tweet():
    executor.submit(do_magic)

    return 'Sending Tweet'


def do_magic():
    artist, song_name, lyrics = prepare_tweet_content()

    tweet = get_tweet_string(artist, song_name, lyrics)

    # Send the tweet
    api.update_status(tweet)


if __name__ == '__main__':
    app.run()
