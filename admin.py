'''
Created on 2013-12-12

@author: zhangzhi
'''

from google.appengine.api import users

import webapp2
import jinja2

import os, logging

from model import *

#logging('home load...')

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates','admin')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#START: RenderPage
class AdminPage(webapp2.RequestHandler):
    def get(self):
        action=self.request.get('action')
        user = users.get_current_user()
        admin_name = user.nickname()
        admin_logout_url = users.create_logout_url('/')

        domain=os.environ['HTTP_HOST']
        baseurl="https://"+domain

        template_values = {
                'admin_name': admin_name,
                'admin_logout_url': admin_logout_url,
        }

        if action=='dashboard':
            template_values.update({'dashboard_active': 'active','admin_title':'Dashboard'})
            template = JINJA_ENVIRONMENT.get_template('admin.html')
        elif action=='charts':
            template_values.update({'charts_active': 'active','admin_title':'Charts'})
            template = JINJA_ENVIRONMENT.get_template('charts.html')
        elif action=='tables':
            template_values.update({'tables_active': 'active','admin_title':'Tables'})
            template = JINJA_ENVIRONMENT.get_template('tables.html')
        elif action=='forms':
            template_values.update({'forms_active': 'active','admin_title':'Forms'})
            template = JINJA_ENVIRONMENT.get_template('forms.html')
        elif action=='typography':
            template_values.update({'typography_active': 'active','admin_title':'Typography'})
            template = JINJA_ENVIRONMENT.get_template('typography.html')
        elif action=='elements':
            template_values.update({'elements_active': 'active','admin_title':'Elements'})
            template = JINJA_ENVIRONMENT.get_template('bootstrap-elements.html')
        elif action=='grid':
            template_values.update({'grid_active': 'active','admin_title':'Grid'})
            template = JINJA_ENVIRONMENT.get_template('bootstrap-grid.html')
        elif action=='blank-page':
            template_values.update({'blank_active': 'active','admin_title':'Blank'})
            template = JINJA_ENVIRONMENT.get_template('blank-page.html')
        else:
            template_values.update({'dashboard_active': 'active','admin_title':'Dashboard'})
            template = JINJA_ENVIRONMENT.get_template('admin.html')

        self.response.write(template.render(template_values))
    '''
    def post(self):
        config = ConfigSite.query().fetch()[0]
        config.title = self.request.get("title")
        if users.get_current_user():
            config.author = users.get_current_user()
        else:
            config.author = users.User("anonymous@xxx.com")
        #config.date already auto set
        config.put()
        welcome = Welcome.query().fetch()[0]
        welcome.words = self.request.get("words")
        welcome.is_show = (self.request.get("is_show") == "True")
        welcome.put()
        self.redirect('/admin')
    '''
#END: RenderPage

# START: Frame
app = webapp2.WSGIApplication([('/admin', AdminPage),
                                  ])
# END: Frame