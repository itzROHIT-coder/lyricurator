import time
from lyrics_util import *


def prepare_tweet_content():
    while True:
        artists = get_artists_links()

        if not artists:
            time.sleep(1)
            continue

        try:
            selected_artist = random.choice(artists)
        except IndexError:
            time.sleep(1)
            continue

        # 'selected_song' is a tuple where 1st is song name and 2nd is its link
        artist_name, selected_song = get_artist_name_and_song(selected_artist)

        if not artist_name or not selected_song:
            time.sleep(1)
            continue

        song_lyrics = get_lyrics(selected_song[1])

        if not song_lyrics:
            time.sleep(1)
            continue

        lyrics_portion = get_lyrics_portion(song_lyrics)

        if lyrics_portion:
            return artist_name, selected_song[0], lyrics_portion


def get_tweet_string(artist_name, song_name, lyrics):
    tweet = '\n'.join(lyrics)
    tweet += '\n\n'
    tweet += artist_name + ' - ' + song_name

    return tweet
