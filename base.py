'''
Created on 2013-12-12

@author: zhangzhi
'''
import webapp2
import jinja2

import os, logging

from functools import wraps

#def requires_admin(method)://requires_admin
#    @wraps(method)
#    def wrapper(self, *args, **kwargs):
#        if not self.is_login:
#            self.redirect(users.create_login_url(self.request.uri))
#            return
#        elif not self.is_admin:
#            return self.error(403)
#        else:
#            return method(self, *args, **kwargs)
#    return wrapper

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates','default')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class BaseRequestHandler(webapp2.RequestHandler):
    pass
