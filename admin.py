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
        document = lxml.html.document_fromstring(content)
        summary = document.text_content()[:50]+'...'
#if action == add(new) edit(not published) udpdate(published)
        article=Article(url=url, title=title, author=author, summary=summary,type='Origin',
                        category='Life', content=content, date=timestamp, archive=archive, 
                        pageid=pageid, slug=slug)
        article.put()
        self.redirect('/admin/listing')
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
        type=self.request.get('type')
        file=self.request.get('upload')
        #name, suffix = file.name.split('.',1)
        #mimetype = file.content_type
        #content=file.read()#could resize pic using PIL lib
        #image = Image(name=name,suffix=suffix,mimetype=mimetype,content=content)
        #logging.info('mimetype='+mimetype)
        #logging.info('name='+name+' suffix='+suffix)
        #logging.info('content='+content)

        '''
        #step 2:redirect to picture tab,then fill pic in blank frame
            funcNum = request.GET.get('CKEditorFuncNum')
            url = get_config()['SERVER_URL'] + "/attachment/" + str(key)
            alt_msg = '' #server alert this message in dialog
            res = '<script type="text/javascript">'
            res += 'window.parent.CKEDITOR.tools.callFunction(%s,"%s","%s");' % (funcNum,url,alt_msg)
            res += '</script>'
            #ok go exec
            response = HttpResponse(res)
            return response
        '''
        self.response.write('<b>type</b>')


# START: Frame
app = webapp2.WSGIApplication([('/admin', AdminPage),
                               ('/admin/listing',ListingPage),
                               ('/admin/setting',SettingPage),
                               ('/admin/upload',UploadPage),
                               ('/admin/(.*)',AdminPage),
                                  ])
# END: Frame
