
from google.appengine.ext import db

class Song(db.Model):
    id = db.Key()
    owner = db.UserProperty()
    name = db.StringProperty(multiline=False)
    author = db.StringProperty(multiline=False)
    album = db.StringProperty(multiline=False)
    albumYear = db.StringProperty(multiline=False)
    uri = db.StringProperty(multiline=False)
    date = db.DateTimeProperty(auto_now_add=True)
    status = db.BooleanProperty()