from subprocess import Popen
import spotipy
import spotipy.util as util
import time


class Spotify():
    def __init__(self, username, client_id, client_secret, redirect_uri, scope):
        #         self.username = username
        #         self.client_id = client_id
        #         self.client_secret = client_secret
        #         self.redirect_uri = redirect_uri
        #         self.scope = 'user-read-playback-state, user-read-currently-playing, user-modify-playback-state'
        self.token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
        self.sp = spotipy.Spotify(auth=self.token)
        self.volume_percent = 60
        self._initial()

    def _initial(self):
        # put local spotify location
        Popen([])
        time.sleep(5)
        # print(self.sp.devices().items())
        for _, vals in self.sp.devices().items():
            for val in vals:
                if (val['type'] == 'Computer'):
                    self.device_id = val['id']

        assert (self.device_id != None), "Computer not found "

        self.sp.volume(volume_percent=self.volume_percent, device_id=self.device_id)

    def search_and_play(self, content):
        """
        artist
        """
        # self.results = self.sp.search(q='artist:' + content, type='artist')
        # self.query = self.sp.artist(self.results['artists']['items'][0]['id'])
        # self.query = self.query['external_urls']['spotify']
        # self.sp.start_playback(device_id=self.device_id, context_uri=self.query)

        """
        playlist
        """
        query = ' '.join(content[1:])
        url = self.sp.search(q=query, type='playlist')['playlists']['items'][0]['external_urls']['spotify']
        self.sp.start_playback(device_id=self.device_id, context_uri=url)
        return "Playing " + query + " from Spotify"



    def next_song(self):
        self.sp.next_track(device_id=self.device_id)
        return "Next song"

    def previous_song(self):
        self.sp.previous_track(device_id=self.device_id)
        return "Previous song"

    def pause(self):
        self.sp.pause_playback(device_id=self.device_id)
        return "Pause the song"

    def resume(self):
        self.sp.start_playback(device_id=self.device_id)
        return "Continue the song"

    def repeat(self):
        self.sp.repeat(state='track', device_id=self.device_id)
        return "Make mode into repeat"

    def no_repeat(self):
        self.sp.repeat(state='off', device_id=self.device_id)
        return "Make mode into non-repeat"

    def shuffle(self):
        self.sp.shuffle(state=True, device_id=self.device_id)
        return "Make mode into shuffle"

    def no_shuffle(self):
        self.sp.shuffle(state=False, device_id=self.device_id)
        return "Make mode into non-shuffle"

    def volume_up(self):
        self.volume_percent = min(self.volume_percent + 20, 100)
        self.sp.volume(volume_percent=self.volume_percent, device_id=self.device_id)
        return "Volume up. Right now: {}% ".format(self.volume_percent)

    def volume_down(self):
        self.volume_percent = max(self.volume_percent - 20, 0)
        self.sp.volume(volume_percent=self.volume_percent, device_id=self.device_id)
        return "Volume down. Right now: {}% ".format(self.volume_percent)


# username = 'Eajay' #placeholder value here
# client_id = 'e9dd65c9d38140498a3257955ef5ebad' #placeholder value here
# client_secret = '3b36025b7ceb44a89778ac081a9839d1' #placeholder value here
# redirect_uri = 'https://www.google.it'
# scope = 'user-read-playback-state, user-read-currently-playing, user-modify-playback-state'
#
# client = Spotify(username=username, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
# client.search_and_play("lady gaga")