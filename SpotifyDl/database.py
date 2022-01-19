from mysql.connector import pooling
from datetime import date
import pickle
import settings
current_date = date.today()
connection_pool = None



def startDatabase():
    beginDatabaseConnection()
    initDatabase()

def initDatabase():
    global connection_pool
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()
    cursor.execute("SET sql_notes = 0; ")
    cursor.execute("CREATE SCHEMA IF NOT EXISTS spotifydb;")
    cursor.execute("USE spotifydb;")
    cursor.execute("SET sql_notes = 0;")
    cursor.execute("set global max_allowed_packet=67108864;")
    cursor.execute("create table IF NOT EXISTS song_bin (song_num int NOT NULL AUTO_INCREMENT, PRIMARY KEY (song_num), song_id varchar(100), date varchar(40), status varchar(100),  songwrapper BLOB, playlist_name varchar(70));")
    cursor.execute("create table IF NOT EXISTS youtube_vid (vid_no int NOT NULL AUTO_INCREMENT, PRIMARY KEY (vid_no), song_id varchar(100), date varchar(40), status varchar(100),  videowrapper MEDIUMBLOB, playlist_name varchar(70));")
    cursor.execute("create table IF NOT EXISTS playlists (num int NOT NULL AUTO_INCREMENT, PRIMARY KEY (num), playlist_name varchar(70), playlistwrapper BLOB);")
    cursor.execute("SET sql_notes = 1; ")

def beginDatabaseConnection():
    global connection_pool
    connection_pool = pooling.MySQLConnectionPool(
        pool_size=32,
        pool_reset_session=True,
        host=settings.databasehost,
        user=settings.databaseuser,
        passwd=settings.databasepassword,
    )
    print("Started database connection")


def addSong(song, playlist_name):
    global connection_pool
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()
    cursor.execute("USE spotifydb;")

    id = song.song_id
    songblob = pickle.dumps(song)
    query = "INSERT INTO song_bin(song_id, date, playlist_name, status, songwrapper) VALUES(%s, %s, %s, 'FOUND', %s);"
    args = (id, current_date, playlist_name, songblob)

    cursor.execute(query, args)

    connection_object.commit()
    cursor.close()
    connection_object.close()

def getAllSavedSongIDs():
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()
    cursor.execute("USE spotifydb;")
    query = "SELECT song_id FROM song_bin;"
    cursor.execute(query)
    result = cursor.fetchall()
    results = []
    for res in result:
        results.append(res)
    cursor.close()
    connection_object.close()
    return results

def addPlaylist(playlist_name, playlist_object):
    global connection_pool
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()
    cursor.execute("USE spotifydb;")
    query = f"INSERT INTO playlists(`playlist_name`, `playlistwrapper`) VALUES(%s, %s);"
    playlistobjectdumped = pickle.dumps(playlist_object)
    args = (playlist_name, playlistobjectdumped)
    cursor.execute(query, args)
    connection_object.commit()
    cursor.close()
    connection_object.close()

def updateStatus(status, song_id):
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()
    cursor.execute("USE spotifydb;")
    query = "UPDATE song_bin SET status = %s WHERE song_id = %s;"
    args = (status, song_id)
    cursor.execute(query, args)
    connection_object.commit()
    cursor.close()
    connection_object.close()

def getSongsByStatus(status):
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()
    cursor.execute("USE spotifydb;")
    query = "SELECT song_id FROM song_bin WHERE status = %s;"
    args = (status, )
    cursor.execute(query, args)
    result = cursor.fetchall()
    results = []
    cursor.close()
    connection_object.close()
    return result

def getDownloadedSongs(status):
    global connection_pool
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()
    cursor.execute("USE spotifydb;")

    query = "select * FROM song_bin WHERE status = %s;"
    args = (status,)

    cursor.execute(query, args)
    result = cursor.fetchall()
    results = []
    for res in result:
        results.append(pickle.loads(res[4]))
    connection_object.commit()
    cursor.close()
    connection_object.close()
    return results

def addVideo(video, song_id):
    global connection_pool
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()
    cursor.execute("USE spotifydb;")
    playlist_name = None
    videoblob = pickle.dumps(video)
    query = "INSERT INTO youtube_vid(song_id, date, playlist_name, status, videowrapper) VALUES(%s, %s, %s, 'READY', %s);"
    args = (song_id, current_date, playlist_name,videoblob)

    cursor.execute(query, args)

    connection_object.commit()
    cursor.close()
    connection_object.close()

def getReadydVideoIDs():
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()
    cursor.execute("USE spotifydb;")
    query = "SELECT song_id FROM youtube_vid where status = READY;"
    cursor.execute(query)
    result = cursor.fetchall()
    results = []
    for res in result:
        results.append(res)
    cursor.close()
    connection_object.close()
    return results

def getReadyVideos(status):
    global connection_pool
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()
    cursor.execute("USE spotifydb;")

    query = "select * FROM youtube_vid WHERE status = %s;"
    args = (status,)

    cursor.execute(query, args)
    result = cursor.fetchall()
    results = []
    for res in result:
        results.append(pickle.loads(res[4]))
    connection_object.commit()
    cursor.close()
    connection_object.close()
    return results

def updateVideoStatus(status, song_id):
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()
    cursor.execute("USE spotifydb;")
    query = "UPDATE youtube_vid SET status = %s WHERE song_id = %s;"
    args = (status, song_id)
    cursor.execute(query, args)
    connection_object.commit()
    cursor.close()
    connection_object.close()

def getAllSavedVideoIDs():
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()
    cursor.execute("USE spotifydb;")
    query = "SELECT song_id FROM youtube_vid;"
    cursor.execute(query)
    result = cursor.fetchall()
    results = []
    for res in result:
        results.append(res)
    cursor.close()
    connection_object.close()
    return results

startDatabase()
initDatabase()

