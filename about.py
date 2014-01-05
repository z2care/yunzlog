'''
Created on 2013-12-12

@author: zhangzhi
'''

from google.appengine.api import users, memcache
from google.appengine.ext import ndb

import webapp2
import jinja2

import os, logging

from model import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates','default')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#START: RenderPage
class AboutPage(webapp2.RequestHandler):
    def get(self):
        domain=os.environ['HTTP_HOST']
        baseurl="https://"+domain
        
        template_values = {
            'page_title': 'About',
            'about_active': 'active',
            'baseurl': baseurl,
        }
        template = JINJA_ENVIRONMENT.get_template('about.html')
        self.response.write(template.render(template_values))
        
#END: RenderPage

# START: Frame
app = webapp2.WSGIApplication([('/about', AboutPage)
                               ], debug=True)
# END: Frame