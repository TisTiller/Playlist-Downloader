import requests, youtube_dl, webbrowser
from base64 import b64encode
from json import load

with open("keys.json", 'r') as keys:
    jsonvals = load(keys)

clientid     = jsonvals['spotify']['clientid']
clientsecret = jsonvals['spotify']['clientsecret']
yt_key       = jsonvals['youtube']['yt_key']

# The Spotify Request Data
data = f"{clientid}:{clientsecret}".encode("utf-8")

# The Playlist To Download
gs = input("Google or Spotify: ").lower()
playlistToDL = input("Playlist ID To Download: ")
if 'g' in gs:
    # Max Youtube Playlist Results
    maxresults = input("Maximum Number of Items: ")


def getSpotifyTracks(playlist_id):
    try:
        r = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers={"Authorization": f"Bearer {sp_key}"})
        print([x['track']['name'] for x in r.json()['items']], sep="\n")
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

videos = []
with youtube_dl.YoutubeDL({}) as ytdl:
    try:
        if 's' in gs:
            ytdl.download([x for x in [youtube_api_search(y) for y in [z['track']['name'] for z in getSpotifyTracks(playlistToDL)['items']]]])
        elif 'g' in gs:
            files = f"https://www.googleapis.com/youtube/v3/playlistItems?key={yt_key}&part=snippet,contentDetails&maxResults={maxresults}&playlistId={playlistToDL}"
            rq = requests.get(files).json()['items']
            for video in rq:
                print(f"{video['snippet']['title']} : https://youtu.be/{video['contentDetails']['videoId']}/")
                videos.append(f"https://youtu.be/{video['contentDetails']['videoId']}/")
            print(f"Items: {len(rq)}")
            ytdl.download([video for video in videos])
    except KeyError as ke:
        print(f"Key Error: (Likely not enough queries left.) \n - {str(ke)}")
