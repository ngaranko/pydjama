
from google.appengine.api import users

from lib.djama import widget

class logged(widget):
    def pre_dispatch(self):
        self.template_vals['user'] = users.get_current_user()
        self.template_vals['url'] = users.create_logout_url('/')
        

class not_logged(widget):
    def pre_dispatch(self):
        self.template_vals['url'] = users.create_login_url('/')