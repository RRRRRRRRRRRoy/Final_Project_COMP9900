# See https://flask.palletsprojects.com/en/2.0.x/config/
from datetime import timedelta

class EMAIL(object):
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'rental.inspection.noreply@gmail.com'
    MAIL_PASSWORD = 'qweasdzxc123..'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = ("Rental_Inspection.com Teams",
                           "rental.inspection.noreply@gmail.com")
    # MAIL_SUPPRESS_SEND = True

## backup email config
# class EMAIL126(object):
#     MAIL_SERVER = 'smtp.126.com'
#     MAIL_PORT = 465
#     MAIL_USERNAME = 'zoeyz2048'
#     MAIL_PASSWORD = 'RRRGXOIGKGVZDRLN'
#     MAIL_USE_TLS = False
#     MAIL_USE_SSL = True
#     MAIL_DEFAULT_SENDER = "zoeyz2048@126.com"
#     # MAIL_SUPPRESS_SEND = True


class CONFIG(EMAIL):
    ENV = 'development'
    DEBUG = True
    SERVER_NAME = 'localhost:5000'
    SECRET_KEY = 'RentalInspection'
    JWT_SECRET_KEY = 'RentalInspection'
    JWT_TOKEN_LOCATION = 'headers'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    SESSION_COOKIE_DOMAIN = False
