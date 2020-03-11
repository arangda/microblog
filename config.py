import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = '273890638@qq.com'
    MAIL_PASSWORD = 'xg273890638'
    ADMINS = ['273890638@qq.com']

    #MAIL_SERVER='localhost'
    #MAIL_PORT=8025

    POSTS_PER_PAGE = 3

    LANGUAGES = ['zh','en']
