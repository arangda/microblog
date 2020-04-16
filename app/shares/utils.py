import os
#import mistune
import secrets
from pygments import highlight
from pygments.lexers import get_lexer_by_name,guess_lexer
from pygments.formatters import HtmlFormatter
#from PIL import Image
from flask_login  import current_user

import re
from unidecode import unidecode
'''
def highlight(html):
    soup = BeautifulSoup(html)
    code_blocks = soup.findAll('pre')
    for block in code_blocks:
        lexer = get_lexer_by_name(block.code['class'][0], stripall=True) if block.code.has_key('class') else guess_lexer(block.text)
        try:
            code = ''.join([item.text for item in block.contents])
            print(block.string)
            formatter = HtmlFormatter(wrapcode=True,cssclass="highlight")
            code_hl = pygments.highlight(code, lexer, formatter)
            
            block.replace_with(BeautifulSoup(code_hl))
            
        except:
            raise
    return Markup(soup)


class MyRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            lexer = guess_lexer(mistune.escape(code.strip()))
        else:
            lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter()
        return highlight(code, lexer, formatter)



def marktohtml(marktext):
    renderer = MyRenderer()
    md = mistune.Markdown(renderer=renderer)
    return md.render(marktext)

def save_image(file):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(file.filename)
    pic_name = random_hex + f_ext

    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads',current_user.username)
    if os.path.isdir(UPLOAD_FOLDER) == False:
        os.mkdir(UPLOAD_FOLDER)
    pic_path = os.path.join(UPLOAD_FOLDER, pic_name)

    im = Image.open(file)
    w,h = im.size
    if w > 640:
        new_w = 640
        new_h = 640 * h/w
    else:
        new_w,new_h = w,h
    im.thumbnail((new_w,new_h))
    im.save(pic_path)
    return pic_name

'''
# 生成slug
from app.thirdapps.baidutransAPI import transit
_punct_re = re.compile(r'[\t !":#$%&\'()*\-\+/<=>?@\[\\\]^_`{|},.]+')
def slugify(text,delim=u'-'):
    newtext = transit(text)
    result = []
    for word in _punct_re.split(newtext.lower()):
        result.extend(unidecode(word).lower().split())
    return delim.join(result)
