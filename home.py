'''
Created on 2013-12-12

@author: zhangzhi
'''

from google.appengine.api import users, memcache
from google.appengine.ext import ndb

import webapp2
import jinja2
import gettext

import os, logging

from model import *

#logging('home load...')

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates','default')),
    extensions=['jinja2.ext.autoescape','jinja2.ext.i18n'],
    autoescape=True)

#START: RenderPage
class HomePage(webapp2.RequestHandler):
    def get(self):
        domain=os.environ['HTTP_HOST']
        baseurl="https://"+domain

        lang = self.request.GET.get('locale', 'zh_CN')

#http://docs.python.org/2/library/gettext.html
#the one way
#        gettext.install('zh_CN', 'locale', unicode=True)
#        tr = gettext.translation('messages', 'locale', languages=['zh_CN'])#languages as list forms
#        tr.install(True)#install _() function,***
#another way
        tr=gettext.translation('messages','locale',fallback=True,languages=['zh_CN'],codeset='utf-8')
        tr.install(unicode=True, names=['gettext', 'ngettext'])

#the same part
        JINJA_ENVIRONMENT.install_gettext_translations(tr)
        template_values = {
            'page_title': 'Home',
            'home_active': 'active',
            'baseurl': baseurl,
        }

        
        template = JINJA_ENVIRONMENT.get_template('home.html')
        self.response.write(template.render(template_values))
        
#END: RenderPage

# START: Frame
app = webapp2.WSGIApplication([('/.*', HomePage)
                               ], debug=True)
# END: Frame
