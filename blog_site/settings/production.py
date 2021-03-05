from .base import *
from decouple import config, Csv

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# DATABASES = {
#   'default': {
#     'ENGINE': 'django.db.backends.postgresql_psycopg2',
#     'NAME': config('DB_NAME'),
#     'USER': config('DB_USER'),
#     'PASSWORD': config('DB_PASSWORD'),
#     'HOST': config('DB_HOST'),
#     'PORT': ,
#   }
# } 

# CACHES = {
#   'default': {
#     'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#     'LOCATION': '127.0.0.1:8000',
#   }
# }

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True