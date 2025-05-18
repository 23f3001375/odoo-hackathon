class Configuartion():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevelopmentConfig(Configuartion):
    SQLALCHEMY_DATABASE_URI= "sqlite:///odoo-hackanthon.db"
    DEBUG = True

    SECRET_KEY= "lets-say-it-is-a-secret" 
    SECURITY_PASSWORD_HASH= "bcrypt"
    SECURITY_PASSWORD_SALT= "$salt-odoo-hackanthon-#$9$"
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-token"