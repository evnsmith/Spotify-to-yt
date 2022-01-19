import os, configparser
import platform

currentPath = os.path.dirname(os.path.realpath(__file__))

#Spotify API
SPOTIPY_USER_ID="evnsmith"
SPOTIPY_CLIENT_ID="7dd262ded5444e23a522a7ec80a337b3"
SPOTIPY_CLIENT_SECRET="0d41a755472f4ba28c32edbe2ed3807f"
REDIRECT_URI="http://localhost"
SCOPE = "user-library-read"

#Genius API
genius_client_id = 'CW5jD19D4E5c333ABbc8yE9J24G13Kv203P2MDdd_BtZKin4RaktnIBkTph_C65T'
genius_client_secret = 'c1cj2cqxOZh6wqyOqOZ3mCsIstQKMrTxmYJTRQAHa3Og6D4fLsEGk5MCH6TZMiVhLEuip2le5s5AmqiLfjpXwg'
genius_access_token = 'DO63H-OZYinSUB-_oMXZyJpX-AOJNf3IWhGZIXAc55jEsDTU19tsLGBIsGC4mnCb'

#mysql database
databasehost = "localhost"
databaseuser = "root"
databasepassword = "Es90290!Es90290!"

input_image_path = '\\Video\\album covers\\'
output_image_path = 'C:\\Users\\evans\\PycharmProjects\\Spotify-to-yt\\Video\\album covers\\'
audio_path = 'C:\\Users\\evans\\PycharmProjects\\Spotify-to-yt\\Video\\audio'
final_video_path = 'C:\\Users\\evans\\PycharmProjects\\Spotify-to-yt\\Video\\final_videos\\'

google_cred_upload = 'C:\\Users\evans\\PycharmProjects\\Spotify-to-yt\\SpotifyDl\\client_secrets.json'
