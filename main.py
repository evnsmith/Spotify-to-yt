from SpotifyDl import spotify
from SpotifyDl import Upload
from SpotifyDl.create import VideoRender
import settings
from SpotifyDl.Upload import UploadVideo
import schedule
import time


playlist_id = '37i9dQZF1DWT0upuUFtT7o'
playlist_name = 'Fresh Finds -  Indie'
render = VideoRender(False)
upload = UploadVideo(settings.google_cred_upload)


def spotify_download():
    """
    upload song data to database and download new songs.
    A database is used to make sure no song is duplicated.

    a lot of the code needs to be formatted better and more efficiently
    """

    song_objects = spotify.add_scripts(playlist_id)
    spotify.download_songs_from_playlist(playlist_id)


def video_render():
    """takes metadata from each song and uses ffmpeg and moviepy to create a video"""

    video_list = render.get_video()
    render.create_video(video_list)

def upload_to_youtube():
    """uploads rendered videos to youtube"""
    songs = spotify.add_scripts(playlist_id)
    videos = Upload.video_data(songs)
    upload.upload()

"""
IN Upload.py CREATE DATABASE FOR VIDEO TITLE, DESCRIPTION, TAGS
"""

upload_to_youtube()



