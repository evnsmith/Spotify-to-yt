import settings
import spotipy
import database
import spotify

TOKEN = spotipy.prompt_for_user_token(

    #username=settings.SPOTIFY_USER_ID,
    client_id=settings.SPOTIPY_CLIENT_ID,
    client_secret=settings.SPOTIPY_CLIENT_SECRET,
    redirect_uri=settings.REDIRECT_URI,
    scope="user-library-read",
)

sp = spotipy.Spotify(auth=TOKEN)



playlist_id = "7vfgcYzHtkunhNz78FtJLA"


spotify.add_scripts(playlist_id)
spotify.download_songs_from_playlist(playlist_id)


videos = database.getReadyVideos("READY")
