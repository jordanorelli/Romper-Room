from conf.base.settings import *
DEBUG = True
TEMPLATE_DEBUG = True

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS += (
    'debug_toolbar',
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'db', 'localdev.sqlite'),
    }
}

#-------------------------------------------------------------------------------
# Foursquare/Facebook deets
#
# here's where we configure our connections to the OAuth servers that we hope
# to connect to.  The variable names are pretty self explanatory.  The redirect
# url can be a bit of a pain since they're validated based on what you put into
# the admin panels for the respective oauth services; it's typical to create
# additional oauth client applications to use in dev or local testing to deal
# with the restrictions on the redirect url.
#-------------------------------------------------------------------------------

FOURSQUARE_CLIENT_ID = ''
FOURSQUARE_CLIENT_SECRET = ''
FOURSQUARE_REDIRECT_URI = ''

FACEBOOK_APP_ID = 0
FACEBOOK_SECRET = ''
FACEBOOK_REDIRECT_URI = ''

AUTHENTICATION_BACKENDS = (
    'dj4sq.backends.FoursquareAuthBackend',
    'fb.backends.FacebookAuthBackend',
)
