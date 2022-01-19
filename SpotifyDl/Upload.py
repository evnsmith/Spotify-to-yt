from itertools import chain
import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from lyricsgenius import Genius
import datetime
import settings
import time
from SpotifyDl import database




class Video:
    def __init__(self,video_file, title, description, tags, song_id):
        self.video_file = video_file
        self.title = title
        self.description = description
        self.tags = tags
        self.category = 10
        self.privacyStatus = 'private'
        self.song_id = song_id

class UploadVideo:

    def __init__(self, CLIENT_SECRET_FILE):


        self.API_NAME = 'youtube'
        self.API_VERSION = 'v3'
        self.SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
        self.CLIENT_SECRET_FILE = CLIENT_SECRET_FILE

    def createService(self):
        print(self.CLIENT_SECRET_FILE, self.API_NAME, self.API_VERSION, self.SCOPES, sep='-')
        CLIENT_SECRET_FILE = self.CLIENT_SECRET_FILE
        API_SERVICE_NAME = self.API_NAME
        API_VERSION = self.API_VERSION
        SCOPES = self.SCOPES
        print(SCOPES)

        cred = None

        pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
        # print(pickle_file)

        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as token:
                cred = pickle.load(token)

        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
                cred = flow.run_local_server()

            with open(pickle_file, 'wb') as token:
                pickle.dump(cred, token)

        try:
            service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
            print(API_SERVICE_NAME, 'service created successfully')
            return service
        except Exception as e:
            print('Unable to connect.')
            print(e)
            return None

    def upload(self,):#, publishAt):
        video_object_list = database.getReadyVideos("READY")
        video = video_object_list[0]
        service = self.createService()



        try:
            database.updateVideoStatus("UPLOADED", video.song_id)

            request_body = {
                'snippet': {
                    'categoryI': video.category,
                    'title': video.title,
                    'description': video.description,
                    'tags': video.tags
                },
                'status': {
                    'privacyStatus': 'public',
                    #'publishAt': publishAt,
                    'selfDeclaredMadeForKids': False,
                },
                'notifySubscribers': False
            }

            mediaFile = MediaFileUpload(video.video_file)

            response_upload = service.videos().insert(
                part='snippet,status',
                body=request_body,
                media_body=mediaFile
            ).execute()
            print("Youtube upload successfully completed.")


        except Exception as e:
            print("Unable to upload.")
            print(e)


            #os.remove(video.video_file)









def video_data(songs):

    video_object_list = []
    ready = database.getAllSavedVideoIDs()
    #print(ready)
    ready = (list(chain.from_iterable(ready)))
    for song in songs:
        if song.song_id in ready:
            #print(song.song_id)
            songs.remove(song)
    #print(len(songs))
    for song in songs:

        song_id = song.song_id
        title = song.song_name + " - " + song.artist_name
        video_file = settings.final_video_path + title + ".mp4"
        #print(video_file)
        tags = song.artist_genres
        tags.append(song.song_name)
        tags.append(song.artist_name)

        genius = Genius(settings.genius_access_token)

        try:
            g_song = genius.search_song(song.song_name, song.artist_name)
            lyrics = g_song.lyrics[:-28]
        except:
            #print("No lyrics found")
            lyrics = ' '

        description = f"\n" \
                      f"{song.artist_name} on Spotify - {song.spotify_artist_url}\n" \
                      f"{song.song_name} - {song.spotify_song_url}\n" \
                      f"\n" \
                      f"\n" \
                      f"{lyrics}" 




        video = Video(video_file,title, description, tags, song_id)
        video_object_list.append(video)
        database.addVideo(video, song_id)
        database.updateStatus("READY",song_id)
        print(video.song_id)

    return video_object_list

def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt

