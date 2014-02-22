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
class ProjectPage(webapp2.RequestHandler):
    def get(self):
        domain=os.environ['HTTP_HOST']
        baseurl="https://"+domain
        
        template_values = {
            'page_title': 'Project',
            'project_active': 'active',
            'baseurl': baseurl,
        }
        template = JINJA_ENVIRONMENT.get_template('projlist.html')
        self.response.write(template.render(template_values))
        
#END: RenderPage

# START: Frame
app = webapp2.WSGIApplication([('/project', ProjectPage)
                               ], debug=True)
# END: Frame