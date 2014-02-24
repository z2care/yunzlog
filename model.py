'''
Created on 2013-12-12

@author: zhangzhi
'''

from google.appengine.api import memcache
from google.appengine.ext import ndb
import logging

logging.info('model loaded...')

class Article(ndb.Model):
    url = ndb.StringProperty()
    slug = ndb.StringProperty(default='')
    title = ndb.StringProperty(default='')
    type = ndb.StringProperty()
    category = ndb.StringProperty()
    author = ndb.UserProperty()
    content = ndb.TextProperty(default='')
    date = ndb.DateTimeProperty()
    pageid = ndb.StringProperty()
    archive = ndb.StringProperty()
    read = ndb.IntegerProperty(default=0)
    summary = ndb.StringProperty(default='')

class Setting(ndb.Model):
    site_title = ndb.StringProperty()
    #site_subtitle = ndb.StringProperty()
    #listmax = ndb.IntegerProperty(default=8)

    def set_cache(self):
      memcache.set('site', self)

    def put(self):
      self.set_cache()
      ndb.Model.put(self)
