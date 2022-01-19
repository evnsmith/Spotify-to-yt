class Playlist():
    def __init__(self, playlist_name, playlist_id, song_count , playlist_url):


        self.playlist_name = playlist_name
        self.playlist_id = playlist_id
        self.song_count = song_count
        self.playlist_url = playlist_url



class Song:

     def __init__(self, artist_name, song_name, song_id, artist_genres, spotify_artist_url, spotify_song_url):
        self.artist_name = artist_name
        self.song_name = song_name
        self.song_id = song_id
        self.artist_genres = artist_genres
        self.spotify_artist_url = spotify_artist_url
        self.spotify_song_url = spotify_song_url




