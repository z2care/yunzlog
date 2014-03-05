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
from base import *

#START: RenderPage
class AboutPage(BaseRequestHandler):
    def get(self):

        template_values = {
            'page_title': 'About',
            'about_active': 'active',
        }
        template_values.update(base_values)
        template = self.get_env.get_template('about.html')
        self.response.write(template.render(template_values))
        
#END: RenderPage

# START: Frame
app = webapp2.WSGIApplication([('/about', AboutPage)
                               ], debug=True)
# END: Frame