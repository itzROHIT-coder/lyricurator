import requests
import bs4
import random
import string
import re

base_url = 'https://www.azlyrics.com/'

user_agents = [
    # Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
    'like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, '
    'like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, '
    'like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, '
    'like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, '
    'like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
    'like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, '
    'like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
    'like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, '
    'like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    # Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR '
    '2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729) '
]


def get_artists_links():
    available_letters = list(string.ascii_lowercase)
    available_letters.append('19')  # To get artists that start with a number
    selected_letter = random.choice(available_letters)

    url = base_url + selected_letter + '.html'
    selected_agent = random.choice(user_agents)
    req = requests.get(url, headers={'User-Agent': selected_agent})

    scraped_objects = bs4.BeautifulSoup(req.content, "html.parser")
    artists_links = []

    for div in scraped_objects.find_all('div',
                                        {'class': 'container main-page'}):
        links = div.find_all('a')

        for a in links:
            artists_links.append(a['href'])

    return artists_links


def get_artist_name_and_song(artist_link):
    url = base_url + artist_link
    selected_agent = random.choice(user_agents)
    req = requests.get(url, headers={'User-Agent': selected_agent})

    scraped_objects = bs4.BeautifulSoup(req.content, "html.parser")
    artist_name = ''
    songs = []

    for strong in scraped_objects.find_all('strong'):
        if strong.parent.name == 'h1':
            artist_name = strong.text.strip()
            break

    # Delete the last word 'Lyrics'
    artist_name = artist_name.rsplit(' ', 1)[0]

    for div in scraped_objects.find_all('div', {'class': 'listalbum-item'}):
        links = div.find_all('a')

        for a in links:
            songs.append((a.text.strip(), a['href'].split('/', 1)[1]))

    try:
        selected_song = random.choice(songs)
    except IndexError:
        selected_song = ''

    if not selected_song:
        return '', ''

    return artist_name, selected_song


def get_lyrics(song_link):
    url = base_url + song_link
    selected_agent = random.choice(user_agents)
    req = requests.get(url, headers={'User-Agent': selected_agent})

    scraped_objects = bs4.BeautifulSoup(req.content, "html.parser")

    lyrics = scraped_objects.find_all('div', attrs={'class': None, 'id': None})

    lyrics = [line.getText() for line in lyrics]
    lyrics = ''.join(lyrics)  # Converting the list to a string
    lyrics = lyrics.split('\n\n')  # Splitting lyrics to individual blocks
    lyrics = [line.strip() for line in lyrics]  # Removing edge spaces

    temp_lyrics = []

    # Removing square brackets
    for line in lyrics:
        formatted_line = re.sub(r'\[.*?\]', '', line)
        formatted_line = formatted_line.strip()

        if formatted_line != '':
            temp_lyrics.append(formatted_line)

    lyrics = temp_lyrics
    temp_lyrics = []

    # Splitting each block into lines
    for block in lyrics:
        temp_lyrics.append(block.split('\n'))

    lyrics = []

    # Last check for special characters
    for block in temp_lyrics:
        temp_block = []
        for line in block:
            formatted_line = line.replace('\r', '')
            formatted_line = formatted_line.replace('\t', '')
            formatted_line = formatted_line.replace('\n', '')
            formatted_line = formatted_line.replace('\\', '')

            if formatted_line != '':
                temp_block.append(formatted_line)

        lyrics.append(temp_block)

    return lyrics


def get_lyrics_portion(lyrics):
    selected_block = random.choice(lyrics)

    # The block is already small to begin with
    if len(selected_block) < 3:
        return selected_block

    # Give a minimum choice space of 3 lyric lines. '-2' because exclusive range
    start_index = random.randrange(0, len(selected_block) - 2)

    # Select from 2 to 3 lines (inclusive) from the selected block
    end_index = start_index + random.randrange(1, 3) + 1

    return selected_block[start_index:end_index]
