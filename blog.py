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

#START: BlogsListPage
class BlogsList(BaseRequestHandler):
    def get(self):
        domain=os.environ['HTTP_HOST']
        baseurl="https://"+domain
        
        articles = Article.query().order(-Article.date).fetch(10, offset=0)

        template_values = {
            'page_title': 'Blog',
            'blog_active': 'active',
            'baseurl': baseurl,
            'articles': articles,
        }
        template = self.get_env.get_template('bloglist.html')
        self.response.write(template.render(template_values))
#END: BlogsListPage
#START: SingleBlogPage
class SingleBlog(BaseRequestHandler):
    def get(self, archive=None, pageid=None):
        domain=os.environ['HTTP_HOST']
        baseurl="https://"+domain
        logging.info(os.environ['PATH_INFO'])
        article = Article.query(Article.url=='/article/'+archive+'/'+pageid).fetch()
        article[0].read += 1
        article[0].put()

        template_values = {
            'page_title': 'Blog',
            'blog_active': 'active',
            'article': article,
            'baseurl': baseurl,            
        }
        template = self.get_env.get_template('singleblog.html')
        self.response.write(template.render(template_values))
#END: SingleBlogPage
class ErrorPage(webapp2.RequestHandler):
    def get(self):
        template = self.get_env.get_template('error404.html')
        self.response.write(template.render())

# START: Frame
app = webapp2.WSGIApplication([('/blog', BlogsList),
                               ('/article/(?P<archive>\d{6})/(?P<pageid>\d{6})', SingleBlog),
                               ('.*',ErrorPage),
                               ], debug=True)
# END: Frame
