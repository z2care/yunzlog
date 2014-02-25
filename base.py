'''
Created on 2013-12-12

@author: zhangzhi
'''
from google.appengine.api import memcache

import webapp2
import jinja2

import os, logging

from functools import wraps
#from webapp2_extras import i18n#need babel package //NA
import gettext

#def requires_admin(method)://requires_admin
#    @wraps(method)
#    def wrapper(self, *args, **kwargs):
#        if not self.is_login:
#            self.redirect(users.create_login_url(self.request.uri))
#            return
#        elif not self.is_admin:
#            return self.error(403)
#        else:
#            return method(self, *args, **kwargs)
#    return wrapper

logging.info('base loaded ...')

#memcatch JINJA_ENVIRONMENT

JINJA_ENVIRONMENT = memcache.get('JINJA_ENVIRONMENT')
logging.info('memcache.get')
if not JINJA_ENVIRONMENT:
    logging.info('memcache.get = not')

    JINJA_ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates','default')),
        extensions=['jinja2.ext.autoescape','jinja2.ext.i18n'], autoescape=True)
#        lang = self.request.GET.get('locale', 'zh_CN')

#http://jinja.pocoo.org/docs/extensions/
#http://docs.python.org/2/library/gettext.html
#the one way
#gettext.install('zh_CN', 'locale', unicode=True)
#tr = gettext.translation('messages', 'locale', languages=['zh_CN'])#languages as list forms
#tr.install(True)#install _() function,***
#another way
    tr=gettext.translation('messages','locale',fallback=True,languages=['zh_CN'],codeset='utf-8')
    tr.install(unicode=True, names=['gettext', 'ngettext'])

#the same part
    JINJA_ENVIRONMENT.install_gettext_translations(tr)
    logging.info('before set')
    memcache.set(key='JINJA_ENVIRONMENT', value='JINJA_ENVIRONMENT')
    logging.info('after set')
class BaseRequestHandler(webapp2.RequestHandler):
#    def get(self):
#        self.request.cookies.get('abc')
    pass
