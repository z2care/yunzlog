'''
Created on 2013-12-12

@author: zhangzhi
'''

from google.appengine.api import users

import webapp2
import jinja2

import os, logging
from datetime import datetime

import gettext

from model import *

#logging('home load...')

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates','admin')),
    extensions=['jinja2.ext.autoescape','jinja2.ext.i18n'], autoescape=True)
tr=gettext.translation('messages','locale',fallback=True,languages=['zh_CN'],codeset='utf-8')
tr.install(unicode=True, names=['gettext', 'ngettext'])

#the same part
JINJA_ENVIRONMENT.install_gettext_translations(tr)

#START: RenderPage
class AdminPage(webapp2.RequestHandler):
    def get(self,item=None):
        logging.info('get arrived')
        action=self.request.get('action')
        user = users.get_current_user()
        admin_name = user.nickname()
        admin_logout_url = users.create_logout_url('/')

        domain=os.environ['HTTP_HOST']
        baseurl="https://"+domain

        template_values = {
                'admin_name': admin_name,
                'admin_logout_url': admin_logout_url,
                'author':user.nickname(),
                'date':datetime.now()
        }
        if item:
            template_values.update({item+'_active': 'active','admin_title':item})
            template = JINJA_ENVIRONMENT.get_template(item+'.html')
        else:
            template_values.update({'article_active': 'active','admin_title':'article'})
            template = JINJA_ENVIRONMENT.get_template('article.html')

        self.response.write(template.render(template_values))

    def post(self,item=None):
        logging.info('post arrived!')
        if users.get_current_user():
            author = users.get_current_user()
        else:
            author = users.User("anonymous@xxx.com")
        title=self.request.get('title')
        date=self.request.get('date')
        summary=self.request.get('summary')
        content=self.request.get("content")
        blog=Blog(title=title,author=author,summary=summary,content=content,date=datetime.now())
        blog.put()
#        self.redirect('/admin')

#END: RenderPage

# START: Frame
app = webapp2.WSGIApplication([('/admin', AdminPage),
                               ('/admin/(.*)',AdminPage),
                                  ])
# END: Frame