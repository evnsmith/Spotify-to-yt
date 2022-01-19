from moviepy.editor import *
from os.path import isfile, join
from os import listdir
from tinytag import TinyTag
import math
import settings
from PIL import Image
import io
import os

class Video:
    def __init__(self, video_name, image, audio, duration):
        self.video_name = video_name
        self.image = image
        self.audio = audio
        self.duration = duration

class VideoRender:
    def __init__(self, isPlaylist):
        self.isPlaylist = isPlaylist
        self.songs = settings.audio_path



    def get_video(self):

        songs = [f for f in listdir(self.songs) if isfile(join(self.songs, f))]

        videos_list = []

        for song in songs:
            try:
                song_path = self.songs+"//"+song
                audio = TinyTag.get(song_path, image=True)
                duration = int(math.ceil(audio.duration))
                title = str(audio.title)
                artist = str(audio.artist)


                if '/' in artist:
                    artist = artist.replace('/',' feat. ')
                video_name = title +" - "+artist

                album_cover = audio.get_image()
                pi = Image.open(io.BytesIO(album_cover))
                pi.save("{output}{title} - {artist}.png".format(output = settings.output_image_path, title = title, artist = artist))
                image = "{output}{title} - {artist}.png".format(output = settings.output_image_path, title = title, artist = artist)

                video = Video(video_name,image,song_path,duration)
                videos_list.append(video)
            except:
                continue

        return videos_list
    def create_video(self, videos_list):


        for video in videos_list:

            image_clip = []
            video_name = video.video_name
            duration = video.duration
            image = video.image
            audio = video.audio

            clip = ImageClip(image).set_duration(duration)
            audioclip = AudioFileClip(audio)



            clip.audio = audioclip
            image_clip.append(clip)

            final_clip = concatenate_videoclips(image_clip)
            final_clip.write_videofile(settings.final_video_path + video_name + ".mp4", fps=24, audio_bitrate='3000k')

            os.remove(video.image)
            os.remove(video.audio)


