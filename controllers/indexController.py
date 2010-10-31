
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import os, re

import urllib2
from google.appengine.api import urlfetch

from models.songs import Song

from lib.djama import action, widget

class indexAction(webapp.RequestHandler):
    def get(self):
        
        songsQuery = Song.all().order('-date')
        songs = songsQuery.fetch(100)
        
        artists = []
        artistsHtml = ''
        for song in songs:
            if song.author and song.author not in artists:
                artists.append(song.author)
                arUrl = re.sub(' ', '_', song.author)
                artistsHtml += '<li>'
                artistsHtml += '<a href="#artists/' + arUrl + '" '
                artistsHtml +=  ' onClick="Player.load(\'/api/songs/author/' + arUrl + '.json\');">'
                artistsHtml += song.author
                artistsHtml += '</a>'
                artistsHtml += '</li>'
        
        
        if users.get_current_user():
          url = users.create_logout_url(self.request.uri)
          url_linktext = 'Logout'
        else:
          url = users.create_login_url(self.request.uri)
          url_linktext = 'Login'
        
    
        template_values = {
          'user': users.get_current_user(),
          'url': url,
          'url_linktext': url_linktext,
          'artists': artistsHtml,
          }
        
        path = os.path.join(os.path.dirname(__file__), '../templates/demo.html')
        self.response.out.write(template.render(path, template_values))

class restyledAction(webapp.RequestHandler):
    def get(self):
        
        songsQuery = Song.all().order('-date')
        songs = songsQuery.fetch(100)
        
        artists = []
        artistsHtml = ''
        for song in songs:
            if song.author and song.author not in artists:
                artists.append(song.author)
                arUrl = re.sub(' ', '_', song.author)
                artistsHtml += '<li>'
                artistsHtml += '<a href="#artists/' + arUrl + '" '
                artistsHtml +=  ' onClick="Player.load(\'/api/songs/author/' + arUrl + '.json\');">'
                artistsHtml += song.author
                artistsHtml += '</a>'
                artistsHtml += '</li>'
        
        
        if users.get_current_user():
          url = users.create_logout_url(self.request.uri)
          url_linktext = 'Logout'
        else:
          url = users.create_login_url(self.request.uri)
          url_linktext = 'Login'
        
    
        template_values = {
          'user': users.get_current_user(),
          'url': url,
          'url_linktext': url_linktext,
          'artists': artistsHtml,
          }
        
        path = os.path.join(os.path.dirname(__file__), '../templates/restyled/index.html')
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

class addAlbumAction(webapp.RequestHandler):
  def get(self):
    if not users.get_current_user():
      self.redirect(users.create_login_url(self.request.uri))
      return
    
    parsedLinks = ()
    
    if 'link' in self.request.params:
        
        url = 'http://www.ex.ua/view/' + self.request.params['link']
        data = ''
        try:
            result = urlfetch.fetch(url)
            if result.status_code == 200:
                data = result.content
            self.response.out.write(result.content)
        except urllib2.URLError, e:
          handleError(e)
        parsedLinks = re.findall(r"href='/get/(\S+)' title='(.*)' rel='nofollow'>(.*)</a>", data)
        
    if len(parsedLinks) == 0:
        path = os.path.join(os.path.dirname(__file__), '../templates/addAlbum.html')
    else:
        path = os.path.join(os.path.dirname(__file__), '../templates/addAlbumSongs.html')
    params = {'authorName':'', 'albumName':'', 'albumYear':'', 'songs':parsedLinks}
    self.response.out.write(template.render(path, {'params':params}))

  def post(self):
    author = self.request.params.get('authorName')
    albumName = self.request.params.get('albumName')
    albumYear = self.request.params.get('albumYear')
    
    for param in self.request.params:
        if 'songName_' == param[0:9]:
            self.response.out.write('<br />%s' % param[9:len(param)])
            try:
                name = self.request.params[param]
                uri = 'http://www.ex.ua/get/' + param[9:len(param)]
                song = Song()
                song.owner = users.get_current_user()
                song.uri = uri
                song.name = name
                song.author = author
                song.album = albumName
                song.albumYear = albumYear
                song.status = True;
                song.put()
            except Exception, e:
                handleError(e)
    
    self.response.out.write('Done. <a href="/">Go and see it</a>')


class alpha(action):
    def get(self):
        
        self._display('alpha/index')
