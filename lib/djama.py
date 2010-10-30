

from google.appengine.ext import webapp

class action(webapp.RequestHandler):
    def _print(self, string):
        self.response.out.write(string)