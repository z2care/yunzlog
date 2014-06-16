'''
Created on 2013-12-12

@author: zhangzhi
'''

from google.appengine.api import users, memcache
from google.appengine.ext import ndb

import webapp2
import jinja2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from StringIO import StringIO
#import cStringIO as StringIO

import os, logging, random

from model import *
from base import *

logging.info('gallery load...')

#START: RenderPage
class GalleryPage(BaseRequestHandler):
    def get(self):
        logging.info('gallerypage arrive')
        domain=os.environ['HTTP_HOST']
        baseurl="https://"+domain
        
        template_values = {
            'page_title': 'Gallery',
            'gallery_active': 'active',
            'baseurl': baseurl,
        }
        template = self.get_env.get_template('gallery.html')
        self.response.write(template.render(template_values))

class MediaPage(BaseRequestHandler):
    def get(self, keyid=None):
        logging.info('mediapage arrive')
        media = ndb.Key('Media',int(keyid)).get()
        if (media and media.data):
            self.response.headers['Content-Type'] = str(media.type)
            self.response.out.write(media.data)
        else:
            self.redirect('/statics/img/noimage.jpg')

class AuthCode(BaseRequestHandler):
    #ref: http://qinxuye.me/article/create-validate-code-image-with-pil/
    _letter_cases = "abcdefghjkmnpqrstuvwxy" # except:i,l,o,z
    _upper_cases = _letter_cases.upper() # upper case letters
    _numbers = ''.join(map(str, range(3, 10))) # numbers
    init_chars = ''.join((_letter_cases, _upper_cases, _numbers)) # all useable chars
    def get(self):
        logging.info('get auth code')

        img, str = self.create_validate_code()

        output = StringIO()
        img.save(output, 'gif')
        img_data = output.getvalue()
        output.close()

        self.response.headers['Content-Type'] = 'image/gif'
        self.response.out.write(img_data)

    def create_validate_code(self, size=(120, 30),
                             chars=init_chars,
                             img_type="GIF",
                             mode="RGB",
                             bg_color=(255, 255, 255),
                             fg_color=(0, 0, 255),
                             font_size=18,
                             font_type="c:\Windows\Fonts\Arial.ttf",
                             length=4,
                             draw_lines=True,
                             n_line=(1, 2),
                             draw_points=True,
                             point_chance = 2):

        width, height = size
        img = Image.new(mode, size, bg_color)
        draw = ImageDraw.Draw(img)

        def get_chars():
            return random.sample(chars, length)

        def create_lines():
            line_num = random.randint(*n_line)

            for i in range(line_num):
                begin = (random.randint(0, size[0]), random.randint(0, size[1]))
                end = (random.randint(0, size[0]), random.randint(0, size[1]))
                draw.line([begin, end], fill=(0, 0, 0))

        def create_points():
            chance = min(100, max(0, int(point_chance)))

            for w in xrange(width):
                for h in xrange(height):
                    tmp = random.randint(0, 100)
                    if tmp > 100 - chance:
                        draw.point((w, h), fill=(0, 0, 0))

        def create_strs():
            c_chars = get_chars()
            strs = ' %s ' % ' '.join(c_chars)

            font = ImageFont.truetype(font_type, font_size)
            font_width, font_height = font.getsize(strs)

            draw.text(((width - font_width) / 3, (height - font_height) / 3),
                        strs, font=font, fill=fg_color)
            return ''.join(c_chars)

        if draw_lines:
            create_lines()
        if draw_points:
            create_points()
        strs = create_strs()

        params = [1 - float(random.randint(1, 2)) / 100,
                  0,
                  0,
                  0,
                  1 - float(random.randint(1, 10)) / 100,
                  float(random.randint(1, 2)) / 500,
                  0.001,
                  float(random.randint(1, 2)) / 500
                  ]
        img = img.transform(size, Image.PERSPECTIVE, params)
     
        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)

        return img, strs
#END: RenderPage

# START: Frame
app = webapp2.WSGIApplication([('/gallery', GalleryPage),
                               ('/gallery/authcode', AuthCode),
                               ('/gallery/(.*)',MediaPage),
                               ], debug=True)
# END: Frame