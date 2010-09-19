#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import db

from controllers import indexController

# Api controllers
from controllers.api import indexApiController, playlistApiController


class Greeting(db.Model):
  author = db.UserProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)
  status = db.BooleanProperty()


class MainPage(webapp.RequestHandler):
  def get(self):
    greetings_query = Greeting.all().order('-date')
    greetings = greetings_query.fetch(10)

    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Login'

    template_values = {
      'greetings': greetings,
      'url': url,
      'url_linktext': url_linktext,
      }

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

class MainLitePage(webapp.RequestHandler):
    def get(self):
        
        path = os.path.join(os.path.dirname(__file__), 'index_lite.html')
        self.response.out.write(template.render(path, {'user':users.get_current_user()}))

class MainDemoPage(webapp.RequestHandler):
    def get(self):
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
          }
        
        path = os.path.join(os.path.dirname(__file__), 'templates/demo.html')
        self.response.out.write(template.render(path, template_values))

class Json(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'json.tpl')
    self.response.out.write(template.render(path, {}))

class Guestbook(webapp.RequestHandler):
  def post(self):
    greeting = Greeting()

    if users.get_current_user():
      greeting.author = users.get_current_user()

    greeting.content = self.request.get('content')
    greeting.status = True
    greeting.put()
    self.redirect('/')


application = webapp.WSGIApplication(
                                     [('/', indexController.indexAction),
                                      ('/beta', indexController.restyledAction),
                                      ('/lite', MainLitePage),
                                      ('/sign', Guestbook),
                                      ('/test', indexController.indexAction),
                                      ('/test/add', indexController.addAction),
                                      ('/add/album', indexController.addAlbumAction),
                                      ('/api/songs/main.json',indexApiController.indexAction),
                                      ('/api/songs/my.json',indexApiController.myAction),
                                      (r'/api/songs/author/(.*)\.json', indexApiController.authorAction),
                                      ('/api/playlist/addToMy.json', playlistApiController.addAction),
                                      ('/api/playlist/removeFromMy.json', playlistApiController.removeFromMyAction),
                                      ('/api/playlist/my.json', playlistApiController.myAction),
                                      ('/main.json', Json)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
