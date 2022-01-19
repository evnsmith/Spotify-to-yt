from SpotifyDl import database
import os
from SpotifyDl import playlist
import spotipy
import settings
from itertools import chain

TOKEN = spotipy.prompt_for_user_token(

    #username=settings.SPOTIFY_USER_ID,
    client_id=settings.SPOTIPY_CLIENT_ID,
    client_secret=settings.SPOTIPY_CLIENT_SECRET,
    redirect_uri=settings.REDIRECT_URI,
    scope="user-library-read",
)

sp = spotipy.Spotify(auth=TOKEN)



def add_scripts(playlist_id):
    song_list = []
    song_object = []
    sp_playlist = sp.playlist_tracks(playlist_id)
    sp_pl_name = sp.playlist(playlist_id)
    playlist_name = sp_pl_name['name']
    songs = sp_playlist['items']
    already_found = database.getSongsByStatus("FOUND")
    already_found = (list(chain.from_iterable(already_found)))

    for i in songs:
        song_list.append(i)
    song_list = [x for x in song_list if x['track']['id'] not in already_found]

    if len(song_list) == 0:
        print("songs have already been found.")

    for i in song_list:
        try:
            artist_uri = i['track']['artists'][0]['uri']
            artist_info =  sp.artist(artist_uri)
            artist_name = i['track']['artists'][0]['name']
            song_name = i['track']['name']
            song_id=i['track']['id']
            artist_genres = artist_info['genres']
            spotify_artist_url=i['track']['album']['artists'][0]['external_urls']['spotify']
            spotify_song_url=i['track']['external_urls']['spotify']

            song_info = playlist.Song(artist_name, song_name, song_id, artist_genres, spotify_artist_url, spotify_song_url)
            song_object.append(song_info)

        except Exception as e:
            print(e)

        database.addSong(song_info, playlist_name)

        print("added "+str(len(song_object))+ " songs from "+playlist_name+".")

    playlist_name = sp_pl_name['name']
    playlist_id = sp_pl_name['id']
    song_count = sp_pl_name['tracks']['total']
    playlist_url = sp_pl_name['external_urls']['spotify']


    playlist_object = playlist.Playlist(playlist_name, playlist_id, song_count, playlist_url)
    database.addPlaylist(playlist_name, playlist_object)

    return song_object


def download_songs_from_playlist(playlist_id):
    path = str(settings.audio_path)
    already_downloaded_list = []
    sp_playlist = sp.playlist_tracks(playlist_id)
    sp_pl_name = sp.playlist(playlist_id)
    playlist_name = sp_pl_name['name']
    songs = sp_playlist['items']
    song_ids = []

    # already_downloaded = database.getSongsByStatus("DOWNLOADED")
    # for song in already_downloaded:
    #     already_downloaded_list.append(song)

    already_downloaded_list = (list(chain.from_iterable(already_downloaded_list)))


    for id in songs:
        song_ids.append(id['track']['id'])

    # for song_id in already_downloaded_list:
    #     if song_id in song_ids:
    #         song_ids.remove(song_id)
    #         print("skipping song - already downloaded")

    playlist_link = 'https://open.spotify.com/playlist/'+str(playlist_id)

    print("starting download...")

    try:
        os.system("spotdl %s -o C:\\Users\\evans\\PycharmProjects\\Spotify-to-yt\Video\\audio" % playlist_link)

        for id in song_ids:
            database.updateStatus("DOWNLOADED", id)
            #print(id)

        print(str(len(song_ids))+" songs downloaded.")
    except Exception as e:
        print(e)


def get_playlist_name(playlist_id):
    sp_playlist = sp.playlist_tracks(playlist_id)
    sp_pl_name = sp.playlist(playlist_id)
    playlist_name = sp_pl_name['name']

    return playlist_name






