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

#logging('home load...')

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates','default')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#START: RenderPage
class HomePage(webapp2.RequestHandler):
    def get(self):
        config = ConfigSite()
        config = ConfigSite.query().fetch()
        welcome = Welcome()
        welcome = Welcome.query().fetch()
        
        domain=os.environ['HTTP_HOST']
        print os.environ
        baseurl="https://"+domain
        
        template_values = {
            'siteconfig': config[0],
            'sitewelcome': welcome[0],
            'baseurl': baseurl,
        }
        template = JINJA_ENVIRONMENT.get_template('home.html')
        self.response.write(template.render(template_values))
        
#END: RenderPage

# START: Frame
app = webapp2.WSGIApplication([('/', HomePage)
                               ], debug=True)
# END: Frame
