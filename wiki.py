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
class WikiPage(BaseRequestHandler):
    def get(self):
        domain=os.environ['HTTP_HOST']
        baseurl="https://"+domain
        
        template_values = {
            'page_title': 'Wiki',
            'wiki_active': 'active',
            'baseurl': baseurl,
        }
        template = self.get_env.get_template('wiki.html')
        self.response.write(template.render(template_values))
        
#END: RenderPage

# START: Frame
app = webapp2.WSGIApplication([('/wiki', WikiPage)
                               ], debug=True)
# END: Frame
