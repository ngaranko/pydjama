
from google.appengine.ext import db
from models.songs import Song

class Playlist(db.Model):
    owner = db.UserProperty()
    name = db.StringProperty(multiline=False)
    date = db.DateTimeProperty(auto_now_add=True)
    status = db.BooleanProperty()
    
class PlaylistSong(db.Model):
    playlist = db.ReferenceProperty(Playlist)
    song = db.ReferenceProperty(Song)

