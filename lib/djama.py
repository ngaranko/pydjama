
import os
import yaml

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


class action(webapp.RequestHandler):
    def _print(self, string):
        self.response.out.write(string)
    
    def _display(self, template_name, template_params = {}):
        
        _template_path = os.path.join(os.path.dirname(__file__), '../templates/%s.tpl' % template_name)
        
        self.init_widgets()
        
        self.template_vals = {}
        self.template_vals['user'] = users.get_current_user()
        
        self.template_vals['widgets'] = self.widgets
        
        self._print(template.render(_template_path, self.template_vals))
    
    def init_widgets(self):
        widgets_config_path = os.path.join(os.path.dirname(__file__), '../configs/widgets.yaml')
        
        self.widgets = {}
        
        try:
            
            widgets_config = yaml.load(open(widgets_config_path, 'r'))
        except Exception, e:
            return
        
        for position in widgets_config:
            self.widgets[position] = []
            
            for widget_init in widgets_config[position]:
                self.init_widget(position, widget_init)
    
    
    def init_widget(self, position, widget_init):
            
            acl = acl_rules()
            
            if 'acl' in widget_init:
                for acl_rule in widget_init['acl']:
                    key = acl_rule.keys()[0]
                    exec("status = acl.%s(acl_rule[key])" % key)
                    if not status:
                        return
            
            try:
                exec('from widgets.%s import %s' % (position, widget_init['name']))
                exec("_w = %s(position, widget_init['name'])" % widget_init['name'])
                        
                _w.pre_dispatch()
                self.widgets[position].append(_w.render())
            except ImportError, e:
                pass # No widget

class widget:
    def __init__(self, position, name):
        # By Default widgets are in footer, since almost all widgets are ajax-based
        self.position = position if position else 'footer'
        
        # Widget name not set, can not create widget without name
        self.name = name if name else None
        
        self.template_vals = {}
        
    def render(self):
        if self.name == None:
            raise NameError('No Widget Name')

        _tpl_path = os.path.join(os.path.dirname(__file__), '../templates/_widgets/')
        
        _tpl_path = ''.join([_tpl_path, self.position, '/', self.name, '.tpl'])
        
        try:
            return template.render(_tpl_path, self.template_vals)
        except Exception, e:
            return ''
    
class acl_rules:
    def auth(self, status):
        logged = True if status == 'user' else False
        
        is_user = False if not users.get_current_user() else True
        
        return True if logged == is_user else False