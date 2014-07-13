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
from base import BaseRequestHandler

#START: BlogsListPage
class BlogsList(BaseRequestHandler):
    def get(self):
        #6 post per page as default
        page=self.request.get('page')
        page=(int(page) if page else 1)#to int 1~&
        size=Article.query(Article.draft==False).count()#0~&
        max=(size/6)+(0 if size%6==0 else 1)#1~&

        articles = Article.query(Article.draft==False).order(-Article.date).fetch(6, offset=int(page-1)*6)
        if articles:
            older = (None if page==max else page+1)
            newer = (None if page==1 else page-1)

        template_values = {
            'page_title': 'Blog',
            'blog_active': 'active',
            'articles': articles,
            'older':older,
            'newer':newer,
        }
        template_values.update(BaseRequestHandler.base_values)
        template = self.get_env.get_template('bloglist.html')
        self.response.write(template.render(template_values))
#END: BlogsListPage
#START: SingleBlogPage
class SingleBlog(BaseRequestHandler):
    def get(self, archive=None, postid=None):
        #logging.info(os.environ['PATH_INFO'])#request path
        article = Article.query(Article.archive==archive, Article.postid==postid).fetch()
        if not article:
            return self.error(404)

        article[0].read += 1
        article[0].put()
        comments = Comment.query(Comment.entry==article[0].key).order(-Comment.date)
        logging.info(comments)

        template_values = {
            'page_title': 'Blog',
            'blog_active': 'active',
            'article': article,
            'comments': comments,
        }
        template_values.update(BaseRequestHandler.base_values)
        template = self.get_env.get_template('singleblog.html')
        self.response.write(template.render(template_values))
#END: SingleBlogPage
#START: BlogsListPage
class BlogsTags(BaseRequestHandler):
    def get(self, link=None):
        #6 post per page as default
        page=self.request.get('page')
        page=(int(page) if page else 1)#to int 1~&
        size=Article.query(Article.draft==False, Article.tags.IN([link])).count()#0~&
        max=(size/6)+(0 if size%6==0 else 1)#1~&

        articles = Article.query(Article.draft==False, Article.tags.IN([link])).order(-Article.date).fetch(6, offset=int(page-1)*6)

        older = (None if page==max else page+1)
        newer = (None if page==1 else page-1)

        template_values = {
            'page_title': 'Blog',
            'blog_active': 'active',
            'articles': articles,
            'older':older,
            'newer':newer,
        }
        template_values.update(BaseRequestHandler.base_values)
        template = self.get_env.get_template('bloglist.html')
        self.response.write(template.render(template_values))
#END: BlogsListPage
#START: BlogCommentPage
class BlogComment(BaseRequestHandler):
    def get(self):
        logging.info('blog comment get arrived')
    def post(self):
        logging.info('blog comment post arrived')

        cmtext=self.request.get('cmtext')
        keyid=self.request.get('keyid')
        ipaddr=self.request.remote_addr
        author=self.request.get('name')
        email=self.request.get('email')
        #if author and email not None, cookie it.

        comment=Comment(entry=ndb.Key('Article',int(keyid)),content=cmtext,ipaddr=ipaddr,author=author,email=email)
        comment.put()
        self.response.write('<h3>%s<small>%s</small></h3><p>%s</p>'%(comment.author,comment.date,cmtext))
#END: BlogCommentPage
# START: Frame
app = webapp2.WSGIApplication([('/blog', BlogsList),
                               ('/blog/(?P<archive>\d{6})/(?P<postid>\d{6})', SingleBlog),
                               ('/blog/tag/(?P<link>\w+)', BlogsTags),
                               ('/blog/comment', BlogComment)
                               ], debug=True)
# END: Frame
