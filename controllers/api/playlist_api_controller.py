
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db
import os, re

from models.songs import Song
from models.playlists import Playlist, PlaylistSong

from lib.djama import action
from lib.json_utils import format_json

class index(action):
  def get(self):
    songsQuery = Song.all().order('-date')
    songs = songsQuery.fetch(100)
    
    songs_json = format_json(songs)
    
    self._print('{"songs":[%s]}' % songs_json)

class add(action):
    def get(self):
        song = Song.get_by_id(int(self.request.params['id']))
        if not song:
            self.response.out.write('no song')
            return
        
        pq = Playlist.all().filter("owner =", users.get_current_user())
        playlists = pq.fetch(1)
        if len(playlists) == 0:
            pl = Playlist()
            pl.owner = users.get_current_user()
            pl.name = 'My'
            pl.status = True
            pl.put()
        else:
            pl = playlists[0]
        
        ps = PlaylistSong()
        ps.playlist = pl
        ps.song = song
        ps.put()
        self._print('done')
        

class remove_from_my(action):
    def get(self):
        sq = Song.all().filter("uri =", self.request.params['uri'])
        songs = sq.fetch(1)
        if len(songs) == 0:
            self.response.out.write('no song')
            return
        else:
            song = songs[0]
        
        pq = Playlist.all().filter("owner =", users.get_current_user())
        playlists = pq.fetch(1)
        if len(playlists) == 0:
            self.response.out.write('no playlist')
            return
        else:
            pl = playlists[0]
        
        ps = PlaylistSong.all().filter("playlist =", pl)
        for lst in ps:
            if lst.song.uri == song.uri:
                db.delete(lst)
        self._print('done')

class my(action):
    def get(self):
        pq = Playlist.all().filter("owner =", users.get_current_user())
        playlists = pq.fetch(1)
        if len(playlists) == 0:
            self.response.out.write('No playlists')
            return
        
        psq = PlaylistSong.all().filter("playlist =", playlists[0])
        psongs = psq.fetch(100)
        songs = []
        for ps in psongs:
            songs.append(ps.song)
        
        songs_json = format_json(songs)
        
        self._print('{"songs":[%s]}' % songs_json)
