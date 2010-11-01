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
from controllers.api import index_api_controller, playlist_api_controller, songs_api_controller

class Json(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'json.tpl')
    self.response.out.write(template.render(path, {}))


application = webapp.WSGIApplication(
                                     [('/', indexController.indexAction),
                                      ('/beta', indexController.restyledAction),
                                      ('/a', indexController.alpha),
                                      ('/test/add', indexController.addAction),
                                      ('/add/album', indexController.addAlbumAction),
                                      ('/api/songs/main.json',index_api_controller.index),
                                      ('/api/songs/my.json',index_api_controller.my),
                                      ('/api/songs/add_song.json', songs_api_controller.add_song),
                                      (r'/api/songs/artist/(.*)\.json', songs_api_controller.artist),
                                      (r'/api/songs/author/(.*)\.json', index_api_controller.author),
                                      ('/api/playlist/add_to_my.json', playlist_api_controller.add),
                                      ('/api/playlist/remove_from_my.json', playlist_api_controller.remove_from_my),
                                      ('/api/playlist/my.json', playlist_api_controller.my),
                                      ('/main.json', Json)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
