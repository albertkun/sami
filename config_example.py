import os
basedir = os.path.abspath(os.path.dirname(__file__))


class EmailServer:
    MAIL_SERVER='mail server'
    MAIL_USERNAME='user name for mail'
    MAIL_PASSWORD='password for mail'
    MAIL_USE_SSL=False
    MAIL_USE_TLS=True



class Config:
    USER = 'USER TO LOGIN'
    DATABASE = 'DATABASE NAME'
    USERNAME = 'USERNAME FOR DATABASE'
    SECRET_KEY = 'DATABASE PASSWORD'
    SSL_DISABLE = False
    HOST = 'HOST
    PORT = 3306
    SALT = 'UNIQUE SALT'
    KEY = 'UNIQUE KEY'

@staticmethod
def init_app(app):
	pass

@classmethod
def init_app(app):
	Config.init_app(app)

config = {

}