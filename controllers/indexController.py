
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import os, re

from models.songs import Song

class indexAction(webapp.RequestHandler):
  def get(self):
    songsQuery = Song.all().order('-date')
    songs = songsQuery.fetch(10)
    
    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Login'

    template_values = {
      'url': url,
      'url_linktext': url_linktext,
      'user': users.get_current_user(),
      'songs': songs
      }

    path = os.path.join(os.path.dirname(__file__), '../templates/index.html')
    self.response.out.write(template.render(path, template_values))

class addAction(webapp.RequestHandler):
  def get(self):
    if not users.get_current_user():
      self.redirect(users.create_login_url(self.request.uri))
      return
        
    path = os.path.join(os.path.dirname(__file__), '../templates/add.html')
    params = {'uri':'', 'songName':'', 'authorName':'', 'albumName':'', 'albumYear':''}
    self.response.out.write(template.render(path, {'params':params}))


  def post(self):
    if not users.get_current_user():
      self.redirect(users.create_login_url(self.request.uri))
      return
    
    neededFields = ('uri', 'songName', 'authorName', 'albumName', 'albumYear')
    errors = {}
    for field in neededFields:
      if field not in self.request.params or self.request.params[field] == '':
        errors[field] = 'Please fill field "' + field + '"'
    
    if len(errors) == 0:
        song = Song()
        song.owner = users.get_current_user()
        song.uri = self.request.params['uri']
        song.name = self.request.params['songName']
        song.author = self.request.params['authorName']
        song.album = self.request.params['albumName']
        song.albumYear = self.request.params['albumYear']
        song.status = True;
        song.put()
        
        self.response.out.write
        path = os.path.join(os.path.dirname(__file__), '../templates/add.html')
        
        if 'isAlbum' not in self.request.params or self.request.params['isAlbum'] != 'on':
            params = {'uri':'', 'songName':'', 'authorName':'', 'albumName':'', 'albumYear':''}
        else:
            params = self.request.params
        
        self.response.out.write(template.render(path, {'params':params}))
    else:
        self.response.out.write(repr(errors))
        self.response.out.write(repr(self.request.params))
