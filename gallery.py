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
class GalleryPage(BaseRequestHandler):
    def get(self):
        domain=os.environ['HTTP_HOST']
        baseurl="https://"+domain
        
        template_values = {
            'page_title': 'Gallery',
            'gallery_active': 'active',
            'baseurl': baseurl,
        }
        template = self.get_env.get_template('gallery.html')
        self.response.write(template.render(template_values))
        
#END: RenderPage

# START: Frame
app = webapp2.WSGIApplication([('/gallery', GalleryPage)
                               ], debug=True)
# END: Frame