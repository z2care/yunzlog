'''
Created on 2013-12-12

@author: zhangzhi
'''

from google.appengine.api import urlfetch, users, memcache
from google.appengine.ext import ndb

import webapp2
import jinja2
from lxml import etree
from lxml.html.clean import Cleaner

import os, logging
from datetime import *

from model import *
from base import BaseRequestHandler

logging.info('home load...')


#START: RenderPage
class HomePage(BaseRequestHandler):
    def get(self): 
        template_values = {
            'page_title': 'Home',
            'home_active': 'active',
        }
        template_values.update(BaseRequestHandler.base_values)
        template = self.get_env.get_template('home.html')
        self.response.write(template.render(template_values))
#END: RenderPage

# START: Frame
app = webapp2.WSGIApplication([('/.*', HomePage)
                               ], debug=True)
# END: Frame
