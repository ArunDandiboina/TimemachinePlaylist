import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SEC = os.environ.get("CLIENT_SEC")
REDIRECT = "https://example.com"
User_NAM = os.environ.get("User_NAM")

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")
bil_web = "https://www.billboard.com/charts/hot-100/"
URL = f"{bil_web}{date}"
res = requests.get(url=URL)

soup = BeautifulSoup(res.text, 'html.parser')
songs = soup.select(selector=".o-chart-results-list-row-container li h3")

soup = BeautifulSoup(res.text, 'html.parser')
playlist = [h3el.getText().strip() for h3el in songs]

# spotify = SpotifyOAuth(client_id=CLIENT_ID,client_secret=CLIENT_SEC,redirect_uri=REDIRECT,scope="playlist-modify-private",cache_path="token.txt",username=User_NAM)
# tok = spotify.get_access_token()

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SEC,
        show_dialog=True,
        cache_path="token.txt",
        username=User_NAM,
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in playlist:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

print(song_uris)
p_id = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=p_id["id"], items=song_uris)
