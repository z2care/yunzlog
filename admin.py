'''
Created on 2013-12-12

@author: zhangzhi
'''

from google.appengine.api import users

import webapp2
import jinja2

import os, logging
from datetime import datetime

from model import *

#logging('home load...')

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates','admin')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#START: RenderPage
class AdminPage(webapp2.RequestHandler):
    def get(self,item=None):
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
        if item=='blog':
            template_values.update({'blog_active': 'active','admin_title':'Blog'})
            template = JINJA_ENVIRONMENT.get_template('blog.html')
        elif action=='dashboard':
            template_values.update({'dashboard_active': 'active','admin_title':'Dashboard'})
            template = JINJA_ENVIRONMENT.get_template('admin.html')
        elif action=='charts':
            template_values.update({'charts_active': 'active','admin_title':'Charts'})
            template = JINJA_ENVIRONMENT.get_template('charts.html')
        elif action=='tables':
            template_values.update({'tables_active': 'active','admin_title':'Tables'})
            template = JINJA_ENVIRONMENT.get_template('tables.html')
        elif action=='forms':
            template_values.update({'forms_active': 'active','admin_title':'Forms'})
            template = JINJA_ENVIRONMENT.get_template('forms.html')
        elif action=='typography':
            template_values.update({'typography_active': 'active','admin_title':'Typography'})
            template = JINJA_ENVIRONMENT.get_template('typography.html')
        elif action=='elements':
            template_values.update({'elements_active': 'active','admin_title':'Elements'})
            template = JINJA_ENVIRONMENT.get_template('bootstrap-elements.html')
        elif action=='grid':
            template_values.update({'grid_active': 'active','admin_title':'Grid'})
            template = JINJA_ENVIRONMENT.get_template('bootstrap-grid.html')
        elif action=='blank-page':
            template_values.update({'blank_active': 'active','admin_title':'Blank'})
            template = JINJA_ENVIRONMENT.get_template('blank-page.html')
        else:
            template_values.update({'dashboard_active': 'active','admin_title':'Dashboard'})
            template = JINJA_ENVIRONMENT.get_template('admin.html')

        self.response.write(template.render(template_values))

    def post(self,item=None):
        if users.get_current_user():
            author = users.get_current_user()
        else:
            author = users.User("anonymous@xxx.com")
        title=self.param('title')
        date=self.param('date')
        summary=self.param('summary')
        content=self.param('content')
        blog=Blog(title=title,author=author,summary=summary,content=content,date=date)
        blog.put()
#        self.redirect('/admin')

#END: RenderPage

# START: Frame
app = webapp2.WSGIApplication([('/admin', AdminPage),
                               ('/admin/(.*)',AdminPage),
                                  ])
# END: Frame