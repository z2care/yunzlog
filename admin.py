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
        user = users.get_current_user()
        config = ConfigSite()
        config = ConfigSite.query().fetch(1)
        welcome = Welcome()
        welcome = Welcome.query().fetch(1)
        print config
        print welcome

        template_values = {
            'siteconfig': config,
            'sitewelcome': welcome,
        }
        template = JINJA_ENVIRONMENT.get_template('admin.html')
        self.response.write(template.render(template_values))

    def post(self):
        config = ConfigSite()
        config.title = self.request.get("site_title")
        if users.get_current_user():
            config.author = users.get_current_user()
        #config.date already auto set
        config.put()
        welcome = Welcome(words=self.request.get("hello"), is_show=True)
        welcome.put()
        self.redirect('/admin')
#END: RenderPage

# START: Frame
app = webapp2.WSGIApplication([('/admin', AdminPage),
                                  ])
# END: Frame