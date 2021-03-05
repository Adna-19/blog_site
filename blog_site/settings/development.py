from .base import *

DEBUG = True

INSTALLED_APPS += [
  'blog.apps.BlogConfig',
  'taggit'
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEBUG_TOOLBAR_CONFIG = {
  'JQUERY_URL': '',
}