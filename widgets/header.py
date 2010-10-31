
from google.appengine.api import users

from lib.djama import widget

class logged(widget):
    def pre_dispatch(self):
        print 'jaaa'
        

class not_logged(widget):
    def pre_dispatch(self):
        self.template_vals['url'] = users.create_login_url('/')