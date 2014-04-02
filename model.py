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
    tags = ndb.StringProperty(repeated=True)
    author = ndb.UserProperty()
    content = ndb.TextProperty(default='')
    date = ndb.DateTimeProperty()
    postid = ndb.StringProperty()
    archive = ndb.StringProperty()
    read = ndb.IntegerProperty(default=0)
    summary = ndb.StringProperty(default='')
    draft = ndb.BooleanProperty(default=False)
    comments = ndb.KeyProperty(kind='Comment', repeated=True)

class Comment(ndb.Model):
	  entry = ndb.KeyProperty(kind=Article, required=True)#use parent instead
	  author = ndb.UserProperty()
	  email = ndb.StringProperty()
	  notify = ndb.BooleanProperty()
	  ipaddr = ndb.StringProperty()
	  date = ndb.DateTimeProperty(auto_now=True)
	  content = ndb.TextProperty(required=True)

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
