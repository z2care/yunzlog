'''
Created on 2013-12-12

@author: zhangzhi
'''
from google.appengine.api import memcache

import webapp2
import jinja2

import os, logging

from functools import wraps
import gettext
from model import *

from datetime import datetime, timedelta

logging.info('base loaded ...')

#JINJA_ENVIRONMENT = memcache.get('JINJA_ENVIRONMENT')
#memcache.set(key='JINJA_ENVIRONMENT', value='JINJA_ENVIRONMENT')
class BaseRequestHandler(webapp2.RequestHandler):

    base_values = {
            'baseurl': "https://"+os.environ['HTTP_HOST'],
    }

    @webapp2.cached_property
    def get_env(self):
        yunzlog_lang = self.request.cookies.get("yunzlog_lang")
        if not yunzlog_lang:
            #could quary defalut language from setting module
            #yunzlog_lang = Setting.query().fetch()[0].default_lang
            yunzlog_lang = 'zh_CN'
            self.response.set_cookie('yunzlog_lang', 'zh_CN', expires=(datetime.now()+timedelta(days=30)), secure=False)

        JINJA_ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates','default')),
        extensions=['jinja2.ext.autoescape','jinja2.ext.i18n'], autoescape=True)

        tr=gettext.translation('messages','locale',fallback=True,languages=[yunzlog_lang],codeset='utf-8')
        tr.install(unicode=True, names=['gettext', 'ngettext'])

        JINJA_ENVIRONMENT.install_gettext_translations(tr)
        return JINJA_ENVIRONMENT
