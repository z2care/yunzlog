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
        
        if user:
            greeting = ('<div style="float:right">Welcome, %s! (<a href="%s">sign out</a>)</div>' %
                        (user.nickname(), users.create_logout_url('/')))
        else:
            greeting = ('<div style="float:right"><a href="%s">Sign in or register</a>.</div>' %
                        users.create_login_url('/'))
        
        self.response.out.write("<br>%s<br><hr>" % greeting)
        
        config = ConfigSite()
        config = ConfigSite.query().fetch()
        welcome = Welcome()
        welcome = Welcome.query().fetch()

        domain=os.environ['HTTP_HOST']
        baseurl="https://"+g_blog.domain

        template_values = {
            'siteconfig': config[0],
            'sitewelcome': welcome[0],
            'username': greeting,
            'baseurl': baseurl,
        }
        
        template = JINJA_ENVIRONMENT.get_template('admin.html')
        self.response.write(template.render(template_values))

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
#END: RenderPage

# START: Frame
app = webapp2.WSGIApplication([('/admin', AdminPage),
                                  ])
# END: Frame