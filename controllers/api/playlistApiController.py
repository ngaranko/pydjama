
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db
import os, re

from models.songs import Song
from models.playlists import Playlist, PlaylistSong

class indexAction(webapp.RequestHandler):
  def get(self):
    songsQuery = Song.all().order('-date')
    songs = songsQuery.fetch(100)
    
    songsJson = ''
    id = 0
    for song in songs:
        songsJson += '{"name":"%s", "author":1, "album":1, "uri":"%s",' % (song.name, song.uri)
        if song.author:
            author = song.author
        else:
            author = 'VA'
        if song.album:
            album = song.album
        else:
            album = 'VA'
            
        songsJson += '"authorName":"%s", "albumName":"%s"}' % (author, album)
        id += 1
        if id != len(songs):
            songsJson += ','
    
    self.response.out.write('{"songs":[%s]}' % songsJson)

class addAction(webapp.RequestHandler):
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
        self.response.out.write('done')

class removeFromMyAction(webapp.RequestHandler):
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
        self.response.out.write('done')

class myAction(webapp.RequestHandler):
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
        
        songsJson = ''
        id = 0
        for song in songs:
            songsJson += '{"name":"%s", "author":1, "album":1, "uri":"%s",' % (song.name, song.uri)
            if song.author:
                author = song.author
            else:
                author = 'VA'
            if song.album:
                album = song.album
            else:
                album = 'VA'
                
            songsJson += '"authorName":"%s", "albumName":"%s"}' % (author, album)
            id += 1
            if id != len(songs):
                songsJson += ','
        
        self.response.out.write('{"songs":[%s]}' % songsJson)
