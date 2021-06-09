import spotipy, time, requests
from pprint import pprint
from flask import Flask, request, url_for, session, redirect
from flask_cors import CORS
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
CORS(app)

app.secret_key = "secret key goes here"
app.config["SESSION_COOKIE_NAME"] = "My cookie"

@app.route("/")
def login():
    spOauth = createSpotifyOauth()
    authURL = spOauth.get_authorize_url()
    return redirect(authURL)

@app.route("/redirect")
def redirectPage():
    spOauth = createSpotifyOauth()
    session.clear()
    code = request.args.get("code")
    tokenInfo = spOauth.get_access_token(code)
    session["token_info"] = tokenInfo
    return redirect(url_for("getBPM", _external=True))

@app.route("/getTracks")
def getTracks():
    try:
        tokenInfo = getToken()
    except:
        print("user not logged in")
        return redirect("/")
    
    sp = spotipy.Spotify(auth=tokenInfo["access_token"])
    return str(sp.current_user_saved_tracks(limit=50, offset=0)["items"][0])

def getToken():
    tokenInfo = session.get("token_info", None)
    if not tokenInfo:
        raise Exception
    now = int(time.time())

    isExpired = tokenInfo["expires_at"] - now < 60
    if isExpired:
        spOauth = createSpotifyOauth()
        tokenInfo = spOauth.refresh_access_token(tokenInfo["refresh_token"])
    return tokenInfo

@app.route("/getBPM")
def getBPM():
    try:
        tokenInfo = getToken()
    except:
        print("user not logged in")
        return redirect("/")
    
    sp = spotipy.Spotify(auth=tokenInfo["access_token"])
    playingSong = sp.currently_playing()
    print(playingSong)
    songID = playingSong["item"]["id"]
    tempo = sp.audio_features(songID)[0]["tempo"]
    messageSent = playingSong["timestamp"]
    songProgress = playingSong["progress_ms"]
    songEnd = (playingSong["item"]["duration_ms"] - songProgress) + (time.time() * 1000) # Timestamp in ms

    requests.get(f"http://192.168.1.124:3000/bpm?mode=spotifyResponse&bpm={tempo}&messageSent={messageSent}&songProgress={songProgress}&songID={songID}")
    return redirect(f"http://192.168.1.124:3000/?bpmLiveUpdate=true&songEnd={songEnd}&currentSongID={songID}")

@app.route("/getCurrentTrack")
def getCurrentTrack():
    try:
        tokenInfo = getToken()
    except:
        print("user not logged in")
        return "Error: Not logged in"
    
    sp = spotipy.Spotify(auth=tokenInfo["access_token"])
    playingSong = sp.currently_playing()["item"]["id"]

    return redirect(f"http://192.168.1.124:3000/?bpmLiveUpdate=true&newSongID={playingSong}")



def createSpotifyOauth():
    return SpotifyOAuth (
        client_id="8d69eb54af404d3b9d29eb60c4dbe71c",
        client_secret="f99ed2b42be346f79e40f7b7cd5340d9",
        redirect_uri=url_for("redirectPage", _external=True),
        scope="user-read-currently-playing"
    )

if __name__ == "__main__":
    app.run(port=8000, debug=True, host="0.0.0.0")