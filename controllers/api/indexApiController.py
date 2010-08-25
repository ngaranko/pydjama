
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import os, re

from models.songs import Song

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

class myAction(webapp.RequestHandler):
    def get(self):
        sq = Song.all().filter("owner =", users.get_current_user())
        songs = sq.fetch(100)
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

class authorAction(webapp.RequestHandler):
    def get(self, authorName):
        authorName = re.sub('_', ' ', authorName)
        
        sq = Song.gql("WHERE author = '%s'" % authorName)
        songs = sq.fetch(100)
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

