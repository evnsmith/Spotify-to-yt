import os, configparser
import platform

currentPath = os.path.dirname(os.path.realpath(__file__))

#Spotify API
SPOTIPY_USER_ID=""
SPOTIPY_CLIENT_ID=""
SPOTIPY_CLIENT_SECRET=""
REDIRECT_URI="http://localhost"
SCOPE = "user-library-read"

#Genius API
genius_client_id = ''
genius_client_secret = ''
genius_access_token = ''

#mysql database
databasehost = "localhost"
databaseuser = "root"
databasepassword = ""

input_image_path = '\\Video\\album covers\\'
output_image_path = '\\Video\\album covers\\'
audio_path = '\\Video\\audio'
final_video_path = '\\Video\\final_videos\\'

google_cred_upload = 'client_secrets.json'
