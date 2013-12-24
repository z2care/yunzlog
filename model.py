'''
Created on 2013-12-12

@author: zhangzhi
'''

from google.appengine.ext import ndb
import logging

#logging('model load...')

class ConfigSite(ndb.Model):
    title = ndb.StringProperty(required=True)
    author = ndb.UserProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class Welcome(ndb.Model):
    words = ndb.StringProperty(required=True)
    is_show = ndb.BooleanProperty(default=True)