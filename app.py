from flask import Flask, redirect, request, session, url_for, render_template, flash
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import json
from dotenv import load_dotenv
import config
from google.oauth2.credentials import Credentials
import time

# Load environment variables
load_dotenv()

# Disable HTTPS requirement for local development
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# Spotify API Settings
sp_oauth = SpotifyOAuth(
    client_id=config.SPOTIFY_CLIENT_ID,
    client_secret=config.SPOTIFY_CLIENT_SECRET,
    redirect_uri=config.SPOTIFY_REDIRECT_URI,
    scope="playlist-read-private playlist-read-collaborative"
)

# YouTube OAuth Settings
def get_youtube_service():
    credentials_dict = session.get("youtube_credentials")
    if not credentials_dict:
        return None
    
    # Recreate credentials from dictionary
    credentials = Credentials(
        token=credentials_dict['token'],
        refresh_token=credentials_dict['refresh_token'],
        token_uri=credentials_dict['token_uri'],
        client_id=credentials_dict['client_id'],
        client_secret=credentials_dict['client_secret'],
        scopes=credentials_dict['scopes']
    )
    
    return build("youtube", "v3", credentials=credentials)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login_spotify")
def login_spotify():
    try:
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    except Exception as e:
        flash(f"Spotify login error: {str(e)}", "error")
        return redirect(url_for("index"))

@app.route("/spotify_callback")
def spotify_callback():
    try:
        code = request.args.get("code")
        token_info = sp_oauth.get_access_token(code)
        session["spotify_token"] = token_info
        
        # Check if YouTube is already logged in
        if "youtube_credentials" not in session:
            flash("Please login to YouTube to continue", "info")
            return redirect(url_for("index"))
            
        return redirect(url_for("dashboard"))
    except Exception as e:
        flash(f"Spotify login error: {str(e)}", "error")
        return redirect(url_for("index"))

@app.route("/login_youtube")
def login_youtube():
    try:
        flow = Flow.from_client_secrets_file(
            config.YOUTUBE_CLIENT_SECRETS_FILE,
            scopes=config.YOUTUBE_SCOPES,
            redirect_uri="http://127.0.0.1:5000/youtube_callback"
        )
        authorization_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true"
        )
        session["youtube_state"] = state
        return redirect(authorization_url)
    except Exception as e:
        flash(f"YouTube login error: {str(e)}", "error")
        return redirect(url_for("index"))

@app.route("/youtube_callback")
def youtube_callback():
    try:
        state = session["youtube_state"]
        flow = Flow.from_client_secrets_file(
            config.YOUTUBE_CLIENT_SECRETS_FILE,
            scopes=config.YOUTUBE_SCOPES,
            state=state,
            redirect_uri="http://127.0.0.1:5000/youtube_callback"
        )
        flow.fetch_token(authorization_response=request.url)
        credentials = flow.credentials
        
        # Convert credentials to a dictionary for session storage
        credentials_dict = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        
        session["youtube_credentials"] = credentials_dict
        return redirect(url_for("dashboard"))
    except Exception as e:
        flash(f"YouTube callback error: {str(e)}", "error")
        return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    # Check if user is logged in to both services
    if "spotify_token" not in session or "youtube_credentials" not in session:
        return redirect(url_for("index"))
    
    try:
        sp = spotipy.Spotify(auth=session["spotify_token"]["access_token"])
        playlists = sp.current_user_playlists()
        
        # Check if user has any playlists
        if not playlists["items"]:
            flash("You don't have any playlists on Spotify", "info")
            return redirect(url_for("index"))
            
        return render_template("dashboard.html", playlists=playlists["items"])
    except Exception as e:
        flash(f"Error fetching playlists: {str(e)}", "error")
        return redirect(url_for("index"))

@app.route("/transfer_playlist", methods=["POST"])
def transfer_playlist():
    try:
        playlist_id = request.form.get("playlist_id")
        if not playlist_id:
            flash("No playlist selected", "error")
            return redirect(url_for("dashboard"))

        sp = spotipy.Spotify(auth=session["spotify_token"]["access_token"])
        playlist = sp.playlist(playlist_id)
        tracks = sp.playlist_tracks(playlist_id)
        
        youtube = get_youtube_service()
        if not youtube:
            flash("YouTube authentication error", "error")
            return redirect(url_for("dashboard"))

        # Create YouTube playlist
        try:
            playlist_body = {
                "snippet": {
                    "title": f"Spotify: {playlist['name']}",
                    "description": f"Transferred from Spotify playlist: {playlist['name']}\nOriginal description: {playlist.get('description', '')}"
                },
                "status": {
                    "privacyStatus": "public"
                }
            }

            playlist_response = youtube.playlists().insert(
                part="snippet,status",
                body=playlist_body
            ).execute()

            youtube_playlist_id = playlist_response["id"]
        except Exception as e:
            if "quotaExceeded" in str(e):
                flash("YouTube API quota exceeded. Please try again tomorrow or request a quota increase from Google Cloud Console.", "error")
            else:
                flash(f"Error creating YouTube playlist: {str(e)}", "error")
            return redirect(url_for("dashboard"))

        success_count = 0
        error_count = 0
        error_details = []
        
        # Process tracks in smaller chunks
        chunk_size = 10  # Process 10 tracks at a time
        total_tracks = len(tracks["items"])
        
        for i in range(0, total_tracks, chunk_size):
            chunk = tracks["items"][i:i + chunk_size]
            
            for item in chunk:
                track = item["track"]
                if not track:
                    continue
                    
                track_name = track["name"]
                artist_name = track["artists"][0]["name"]
                query = f"{track_name} {artist_name} official"
                
                try:
                    # Add delay between requests to avoid quota issues
                    time.sleep(2)  # 2 second delay between requests
                    
                    search_response = youtube.search().list(
                        q=query,
                        part="snippet",
                        maxResults=1,
                        type="video"
                    ).execute()

                    if search_response["items"]:
                        video_id = search_response["items"][0]["id"]["videoId"]
                        try:
                            youtube.playlistItems().insert(
                                part="snippet",
                                body={
                                    "snippet": {
                                        "playlistId": youtube_playlist_id,
                                        "resourceId": {
                                            "kind": "youtube#video",
                                            "videoId": video_id
                                        }
                                    }
                                }
                            ).execute()
                            success_count += 1
                        except Exception as e:
                            if "quotaExceeded" in str(e):
                                flash(f"YouTube API quota exceeded after transferring {success_count} tracks. Please try again tomorrow to transfer the remaining tracks.", "warning")
                                return render_template("result.html", 
                                                     playlist_link=f"https://www.youtube.com/playlist?list={youtube_playlist_id}",
                                                     success_count=success_count,
                                                     error_count=error_count,
                                                     error_details=error_details)
                            error_count += 1
                            error_details.append(f"'{track_name}' by {artist_name} - Error adding to playlist: {str(e)}")
                    else:
                        error_count += 1
                        error_details.append(f"'{track_name}' by {artist_name} - No matching video found")
                except Exception as e:
                    error_count += 1
                    error_details.append(f"'{track_name}' by {artist_name} - Error: {str(e)}")
                    if "quotaExceeded" in str(e):
                        flash(f"YouTube API quota exceeded after transferring {success_count} tracks. Please try again tomorrow to transfer the remaining tracks.", "warning")
                        return render_template("result.html", 
                                             playlist_link=f"https://www.youtube.com/playlist?list={youtube_playlist_id}",
                                             success_count=success_count,
                                             error_count=error_count,
                                             error_details=error_details)
                    continue

                # Update progress
                progress = ((i + len(chunk)) / total_tracks) * 100
                session['transfer_progress'] = {
                    'current': i + len(chunk),
                    'total': total_tracks,
                    'success': success_count,
                    'error': error_count
                }

        return render_template("result.html", 
                             playlist_link=f"https://www.youtube.com/playlist?list={youtube_playlist_id}",
                             success_count=success_count,
                             error_count=error_count,
                             error_details=error_details)
    except Exception as e:
        flash(f"Error transferring playlist: {str(e)}", "error")
        return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)
