import spotipy
import argparse
import logging
import pylast
import calendar
import datetime as dt
from datetime import datetime
from spotipy.oauth2 import SpotifyOAuth

#logger = logging.getLogger('examples.create_playlist')
#logging.basicConfig(level='DEBUG')

#API keys for Last.fm
API_KEY = "x"  
API_SECRET = "x"

#spotify API keys
client_id="x"
client_secret="x"
redirect_uri="https://www.spotify.com/us/home",


# adds track to a specified playlist, searches by track and artist names through the spotify database
def addTrackByName(sp, playlist_id, track_name, artist):
    print("Adding song -", track_name, artist)
    tracks = sp.search(track_name, type="track", limit=10)
    for i, t in enumerate(tracks['tracks']['items']):
        print(' ', i, t['name'], t['id'])
        name = t['name']
        id = t['id']
        if name == track_name:
            print("checking artists - - - -")
            for j, k in enumerate(t['artists']):
                artist_name = k['name']
                print("comparing -" + str(artist_name) + "-" +str(artist_name) + "-")
                if str(artist_name) == str(artist):
                    print("adding song to playlist", id)
                    id_list = [id]
                    sp.playlist_add_items(playlist_id, id_list)
                    return

# creates a new playlist and returns the playlist id
def createNewPlaylist(sp, playlist_name):

    #Authorize spotify so we can do shit
    #sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="x",
         #                                       client_secret="x",
      #                                          redirect_uri="https://www.spotify.com/us/home/",
       #                                         scope="playlist-modify-public"))
    user_id = sp.me()['id']

    #create playlist and return id
    playlist_data = sp.user_playlist_create(user_id, playlist_name)
    return playlist_data['id']


def main():

    #Authorize spotify so we can do shit
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="x",
                                                client_secret="x",
                                                redirect_uri="https://www.spotify.com/us/home/",
                                                scope="user-library-read playlist-modify-public"))
    
    #Authorize Last.fm
    username = "x"
    password_hash = pylast.md5("x")


    network = pylast.LastFMNetwork(
        api_key=API_KEY,
        api_secret=API_SECRET,
        username=username,
        password_hash=password_hash,
    )

    #get all of the tracks from the specified date range, in this case, as many records as possible
    lastfm_user = network.get_user("bhllamoreaux")
    tracks = lastfm_user.get_recent_tracks(limit=None, cacheable=True)

    #filter tracks by month
    currMonth = "JKL"
    songs = dict()
    for track in tracks:
        #set up for the first loop
        if currMonth == "JKL":
            currMonth = track.playback_date[3:6]
            monthly_playlist_name = track.playback_date[3:11]

        #if we are into a new month, print top tracks, create new playlist for that month and add songs to that playlist
        if track.playback_date[3:6] != currMonth:           

            print("\n Adding tracks for", monthly_playlist_name, " \n")

            #print top tracks for that month and add to playlist

            # create new playlist for the month
            new_playlist_id = createNewPlaylist(sp, monthly_playlist_name)

            #add top 30 tracks to playlist
            sorted_list = dict(sorted(songs.items(), key=lambda item: item[1], reverse=True))

            keys = list(sorted_list)
            i = 0
            while i < 40 and i < len(keys):
                addTrackByName(sp, new_playlist_id, keys[i][0], keys[i][1])
                i += 1
                
            #reset songs dict for the next month
            songs.clear()

            monthly_playlist_name = track.playback_date[3:11]
            currMonth = track.playback_date[3:6]

        # track the number of plays for that song, store in a dict with the key being the artist name and song title
        key = (track.track.get_title(), track.track.get_artist())
        if songs.get(key) == None:
            songs[key] = 1
        else:
            songs[key] = songs[key] + 1

    


if __name__ == '__main__':
    main()
