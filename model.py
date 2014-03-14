'''
Created on 2013-12-12

@author: zhangzhi
'''

from google.appengine.api import memcache
from google.appengine.ext import ndb
import logging

logging.info('model loaded...')

class Article(ndb.Model):
    title = ndb.StringProperty(default='')
    type = ndb.StringProperty()
    tag = ndb.StringProperty(repeated=True)
    author = ndb.UserProperty()
    content = ndb.TextProperty(default='')
    date = ndb.DateTimeProperty()
    postid = ndb.StringProperty()
    archive = ndb.StringProperty()
    read = ndb.IntegerProperty(default=0)
    summary = ndb.StringProperty(default='')
    draft = ndb.BooleanProperty(default=False)

class Setting(ndb.Model):
    site_title = ndb.StringProperty()
    #site_subtitle = ndb.StringProperty()
    #listmax = ndb.IntegerProperty(default=8)
    default_lang = ndb.StringProperty(default='zh_CN')

    def set_cache(self):
      memcache.set('site', self)

    def put(self):
      self.set_cache()
      ndb.Model.put(self)

class Media(ndb.Model):
    data = ndb.BlobProperty()
    name = ndb.StringProperty()
    type = ndb.StringProperty()
