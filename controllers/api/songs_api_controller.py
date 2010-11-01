
from google.appengine.api import users

from lib.djama import action

from models.songs import Song

class add_song(action):
    def get(self):
        self._print('eee')
    def post(self):
        if not users.get_current_user():
            self._print('{"status":"0", "message":"Not logged"}')
        
        errors = False
        params = {}
        for field in ['song_name', 'author_name', 'album_name', 'album_year', 'song_uri']:
            if self.request.params.get(field):
                params[field] = self.request.params.get(field)
            else:
                errors = True
        
        if not errors:
            song = Song()
            song.owner = users.get_current_user()
            song.uri = params['song_uri']
            song.name = params['song_name']
            song.author = params['author_name']
            song.album = params['album_name']
            song.albumYear = params['album_year']
            song.status = True;
            song.put()
        
            self._print('{"status":"1", "message":"Added successully"}')
        else:
            self._print('{"status":"0", "message":"Not all fields are filled"}')