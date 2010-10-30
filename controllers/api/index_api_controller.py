
from google.appengine.api import users
import os, re

from models.songs import Song

from lib.djama import action
from lib.json_utils import format_json


class index(action):
    def get(self):
        songsQuery = Song.all().order('-date')
        songs = songsQuery.fetch(100)
    
        songs_json = format_json(songs)
    
        self._print('{"songs":[%s]}' % songs_json)

class my(action):
    def get(self):
        sq = Song.all().filter("owner =", users.get_current_user())
        songs = sq.fetch(100)
        
        songs_json = format_json(songs)
        
        self._print('{"songs":[%s]}' % songs_json)

class author(action):
    def get(self, authorName):
        authorName = re.sub('_', ' ', authorName)
        
        #sq = Song.gql("WHERE author = '%s' ORDER BY date ASC" % authorName)
        sq = Song.all().filter("author =", authorName).order("date")
        songs = sq.fetch(100)
        
        songs_json = format_json(songs)
        
        self._print('{"songs":[%s]}' % songs_json)

