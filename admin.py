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
        user = users.get_current_user()
        admin_name = user.nickname()
        admin_logout_url = users.create_logout_url('/')

        domain=os.environ['HTTP_HOST']
        baseurl="https://"+domain

        action=self.request.get('action')
        if not action:
          action = 'add'

        template_values = {
                'admin_name': admin_name,
                'admin_logout_url': admin_logout_url,
                'author':user.nickname(),
                'date':datetime.now(),
                'action':action
        }

        if item:
            template_values.update({item+'_active': 'active','admin_title':item})
            template = JINJA_ENVIRONMENT.get_template(item+'.html')
        else:
            template_values.update({'article_active': 'active','admin_title':'article'})
            template = JINJA_ENVIRONMENT.get_template('article.html')

        self.response.write(template.render(template_values))


#END: RenderPage

class SettingPage(webapp2.RequestHandler):
    def get(self):
        logging.info('setting get arrived')
        user=users.get_current_user()
        admin_name = user.nickname()
        admin_logout_url = users.create_logout_url('/')

        domain=os.environ['HTTP_HOST']
        baseurl="https://"+domain

        #articles = Setting.query().fetch()
        setting = Setting(site_title='test title for setting2')
        setting.put()

        template_values = {
                'admin_name': admin_name,
                'admin_logout_url': admin_logout_url,
                'author':user.nickname(),
                'date':datetime.now(),
                'setting':setting
        }


        template_values.update({'setting_active': 'active','admin_title':'setting'})
        template = JINJA_ENVIRONMENT.get_template('blank-page.html')

        self.response.write(template.render(template_values))

class ListingPage(webapp2.RequestHandler):
    def get(self):
        logging.info('listing get arrived')
        user = users.get_current_user()
        admin_name = user.nickname()
        admin_logout_url = users.create_logout_url('/')

        domain=os.environ['HTTP_HOST']
        baseurl="https://"+domain

        articles = Article.query().order(-Article.date).fetch(10, offset=0)

        template_values = {
                'admin_name': admin_name,
                'admin_logout_url': admin_logout_url,
                'author':user.nickname(),
                'date':datetime.now(),
                'articles':articles
        }


        template_values.update({'listing_active': 'active','admin_title':'listing'})
        template = JINJA_ENVIRONMENT.get_template('listing.html')

        self.response.write(template.render(template_values))

class UploadPage(webapp2.RequestHandler):
    def post(self,type=None):       
        fileinfo=self.request.POST['upload']
        media = Media(name=fileinfo.filename,data=fileinfo.value,type=fileinfo.type)
        key=media.put()
        
        #step 2:redirect to picture tab,then fill pic in blank frame
        funcNum = self.request.GET.get('CKEditorFuncNum')
        url = "/gallery/" + str(key.integer_id())
        alt_msg = 'success!zz!' #server alert this message in dialog
        res = '<script type="text/javascript">'
        res += 'window.parent.CKEDITOR.tools.callFunction(%s,"%s","%s");' % (funcNum, url, alt_msg)
        res += '</script>'        
        self.response.write(res)

class ArticlePage(webapp2.RequestHandler):
    def get(self, archive=None, postid=None):
        user = users.get_current_user()
        admin_name = user.nickname()
        admin_logout_url = users.create_logout_url('/')

        action=self.request.get('action')# !!!!!got param action failed
        if not action:
            action = 'add'
            article = None
        elif action == 'edit':
            article = Article.query(Article.url=='/article/'+archive+'/'+postid).fetch()

        template_values = {
                'admin_name': admin_name,
                'admin_logout_url': admin_logout_url,
                'author':user.nickname(),
                'date':datetime.now(),
                'action':action,
                'article':article,
        }

        template_values.update({'article_active': 'active','admin_title':'article'})
        template = JINJA_ENVIRONMENT.get_template('article.html')

        self.response.write(template.render(template_values))

    def post(self,item=None):
        logging.info('post arrived!')
        action=self.request.get('action')
        if action == 'add':
              if users.get_current_user():
                  author = users.get_current_user()
              else:
                  author = users.User("anonymous@xxx.com")

        title=self.request.get('title')

        timestamp=datetime.now()
        archive=timestamp.strftime('%Y%m')
        pageid=timestamp.strftime('%d%H%M')
        url=os.path.join('/article', archive, pageid).replace('\\','/')

        slug=self.request.get('slug')

        content=self.request.get("content")
#        summary=content[:10]
        #document = lxml.html.document_fromstring(content)
        #summary = document.text_content()[:50]+'...'
        summary=content
#if action == add(new) edit(not published) udpdate(published)
        article=Article(url=url, title=title, author=author, summary=summary,type='Origin',
                        category='Life', content=content, date=timestamp, archive=archive, 
                        pageid=pageid, slug=slug)
        article.put()
        self.redirect('/admin/listing')


# START: Frame
app = webapp2.WSGIApplication([('/admin', AdminPage),
                               ('/admin/upload',UploadPage),
                               ('/admin/listing',ListingPage),
                               ('/admin/setting',SettingPage),
                               ('/admin/article',ArticlePage),
                               ('/admin/article/(?P<archive>\d{6})/(?P<pageid>\d{6})',ArticlePage),
                               ('/admin/(.*)',AdminPage),
                                  ])
# END: Frame
