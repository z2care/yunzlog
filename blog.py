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
    def get(self,url=None):
        domain=os.environ['HTTP_HOST']
        baseurl="https://"+domain
        logging.info('url='+baseurl+'/blog/'+url)
        article = Article.query(Article.url=='/blog/'+url).fetch()
        article[0].read += 1
        article[0].put()

        template_values = {
            'page_title': 'Blog',
            'blog_active': 'active',
            'article': article,
            'baseurl': baseurl,            
        }
        template = JINJA_ENVIRONMENT.get_template('singleblog.html')
        self.response.write(template.render(template_values))
#END: SingleBlogPage
class ErrorPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('error404.html')
        self.response.write(template.render())

# START: Frame
app = webapp2.WSGIApplication([('/blog', BlogsList),
                               ('/blog/(.*)', SingleBlog),
                               ('.*',ErrorPage),
                               ], debug=True)
# END: Frame
