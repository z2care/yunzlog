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
from base import *

logging.info('home load...')


#START: RenderPage
class HomePage(webapp2.RequestHandler):
    def get(self): 

        domain=os.environ['HTTP_HOST']
        baseurl="https://"+domain

        show_alert = self.request.cookies.get("show_alert")
        mycookies = self.request.headers.get('Cookie')
        if mycookies:
            logging.info('mycookies='+mycookies+'===')
        if show_alert:
            logging.info('show_alert='+show_alert+'===')

        template_values = {
            'page_title': 'Home',
            'home_active': 'active',
            'baseurl': baseurl,
        }

        template = JINJA_ENVIRONMENT.get_template('home.html')
        self.response.set_cookie('show_alert', 'value_zz', 
          expires=(datetime.now()+timedelta(days=100)), secure=False)
        self.response.write(template.render(template_values))

#END: RenderPage

# START: Frame
app = webapp2.WSGIApplication([('/.*', HomePage)
                               ], debug=True)
# END: Frame
