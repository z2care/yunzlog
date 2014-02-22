'''
Created on 2013-12-12

@author: zhangzhi
'''

from google.appengine.api import memcache
from google.appengine.ext import ndb
import logging

logging.info('model loaded...')

class Blog(ndb.Model):
    title = ndb.StringProperty()
    type = ndb.StringProperty()
    category = ndb.StringProperty()
    author = ndb.UserProperty()
    content = ndb.TextProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    read = ndb.IntegerProperty(default=0)
    summary = ndb.StringProperty()

class Welcome(ndb.Model):
    words = ndb.StringProperty(required=True)
    is_show = ndb.BooleanProperty(default=True)

    def cache_set(self):
        memcache.set(self.key().name(), self, namespace=self.key().kind())
    def put(self):
        self.cache_set()
        ndb.Model.put(self)
