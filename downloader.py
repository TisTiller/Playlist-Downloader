import requests, youtube_dl, webbrowser
from base64 import b64encode

# The Spotify API Client ID & Secret
clientid = ""
clientsecret = ""

# The Youtube API Auth Key.
yt_key = ""

data = f"{clientid}:{clientsecret}".encode("utf-8")

playlistToDL = input("Spotify Playlist ID To Download: ")


def getSpotifyTracks(playlist_id):
    try:
        r = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers={"Authorization": f"Bearer {sp_key}"})
        return r.json()
    except:
        return None

def youtube_api_search(query):
    params = {"q": query, "part": "id", "key": yt_key, "maxResults": 1, "type": "video"}
    yt_url = "https://www.googleapis.com/youtube/v3/search"
    try:
        r = requests.get(yt_url, params=params)

        search_response = r.json()
    except RuntimeError:
        print("GONNA RETURN NONE")
        return None
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            print(f"{query} : https://www.youtube.com/watch?v={search_result['id']['videoId']}")
            return "https://www.youtube.com/watch?v={}".format(search_result["id"]["videoId"])


ar = requests.post(
                "https://accounts.spotify.com/api/token", 
                data={"grant_type": "client_credentials"}, 
                headers={"Authorization": f"Basic {str(b64encode(data), 'utf-8')}"}
                ).json()
if not ar['access_token']:
    print("Didn't get an access token!")
else:
    sp_key = ar['access_token']


# This Comment is equal to the last two lines.

#trackNames = [x['track']['name'] for x in getSpotifyTracks("2YkD1uNBGI8BcBEOEOCf05")['items']]
#trackURLS = []
#for x in trackNames:
#    trackURLS.append(youtube_api_search(x))
#ydl_opts = {}
#with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#    ydl.download([x for x in trackURLS])

with youtube_dl.YoutubeDL({}) as ytdl:
    ytdl.download([x for x in [youtube_api_search(y) for y in [z['track']['name'] for z in getSpotifyTracks(playlistToDL)['items']]]])