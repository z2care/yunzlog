'''
Created on 2013-12-12

@author: zhangzhi
'''

from google.appengine.api import users

import webapp2
import jinja2
import lxml.html

import os, logging
from datetime import datetime

import gettext

from model import *

#logging('admin load...')
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates','admin')),
    extensions=['jinja2.ext.autoescape','jinja2.ext.i18n'], autoescape=True)

tr=gettext.translation('messages','locale',fallback=True,languages=['zh_CN'],codeset='utf-8')
tr.install(unicode=True, names=['gettext', 'ngettext'])

JINJA_ENVIRONMENT.install_gettext_translations(tr)

user = users.get_current_user()
admin_name = user.nickname()
admin_logout_url = users.create_logout_url('/')
admin_values = {
        'admin_name': admin_name,
        'admin_logout_url': admin_logout_url,
}

#START: RenderPage
class AdminPage(webapp2.RequestHandler):
    def get(self):

        logging.info('adminpage get arrived')
        user = users.get_current_user()
        admin_name = user.nickname()
        admin_logout_url = users.create_logout_url('/')

        template_values = {
            'main_active':'active',
            'admin_title':'article',
        }
        template_values.update(admin_values)
        template = JINJA_ENVIRONMENT.get_template('blank-page.html')

        self.response.write(template.render(template_values))

class ArticlePage(webapp2.RequestHandler):
    def get(self, archive=None, postid=None):
        logging.info('articlepage get arrived')

        action=self.request.get('action')
        article = Article.query(Article.archive==archive,Article.postid==postid).fetch()

        if action == 'delete':
            article[0].key.delete()
            self.redirect('/admin/listing/article')

        template_values = {
                'author':user.nickname(),
                'date':datetime.now(),
                'article':article,
        }
        template_values.update(admin_values)
        template_values.update({'article_active': 'active','admin_title':'article'})
        template = JINJA_ENVIRONMENT.get_template('article.html')

        self.response.write(template.render(template_values))

    def post(self,item=None):
        logging.info('articlepage post arrived!')
        submit=self.request.get('button')
        #if submit == 'Save':#Save or Pub
        draft=(True if submit=='Save' else False)

        title=self.request.get('title')
        author = users.get_current_user()

        timestamp=datetime.now()
        archive=timestamp.strftime('%Y%m')
        postid=timestamp.strftime('%d%H%M')

        type=self.request.get("type")

        tag=self.request.get("tag")
        tag=([] if tag else tag.splite(';'))

        content=self.request.get("content")
        document = lxml.html.document_fromstring(content)
        summary = document.text_content()[:30]+'...'

#if action == add(new) edit(not published) udpdate(published)
        article=Article(title=title, author=author, summary=summary,type=type,
                        tag=tag, content=content, date=timestamp, archive=archive,
                        postid=postid, draft=draft)
        article.put()
        self.redirect('/admin/listing/article')

class SettingPage(webapp2.RequestHandler):
    def get(self):
        logging.info('setting get arrived')

        #articles = Setting.query().fetch()
        setting = Setting(site_title='test title for setting2')
        setting.put()

        template_values = {
                'author':user.nickname(),
                'date':datetime.now(),
                'setting':setting
        }

        template_values.update(admin_values)
        template_values.update({'setting_active': 'active','admin_title':'setting'})
        template = JINJA_ENVIRONMENT.get_template('blank-page.html')

        self.response.write(template.render(template_values))

class ListPage(webapp2.RequestHandler):
    def get(self,item=None):
        logging.info('listing get arrived')

        articles = Article.query().order(-Article.date).fetch(10, offset=0)

        template_values = {
                'author':user.nickname(),
                'date':datetime.now(),
                'articles':articles
        }

        template_values.update(admin_values)
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
#END: RenderPage

# START: Frame
app = webapp2.WSGIApplication([('/admin/editing/article',ArticlePage),
                               ('/admin/editing/article/(?P<archive>\d{6})/(?P<postid>\d{6})',ArticlePage),
#                               ('/admin/editing/wiki',WiKiPage),
#                               ('/admin/editing/wiki/(?P<package>\w+)/(?P<class>\w+)/(?P<medhod>\w+)',WiKiPage),
                               ('/admin/listing/(article|wiki|comment)',ListPage),
                               ('/admin/setting',SettingPage),
                               ('/admin/upload',UploadPage),                               
#                               ('/admin/(.*)',ErrorPage),
                               ('/admin|/admin/main', AdminPage),
                                  ])
# END: Frame
