from .settings import *  # noqa
import os

dbhost = os.environ['PGHOST']
dbname = os.environ['PGDATABASE']
dbuser = os.environ['PGUSER']
dbpassword = os.environ['PGPASSWORD']
dbport = os.environ['PGPORT']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': dbname,
        'USER': dbuser,
        'PASSWORD': dbpassword,
        'HOST': dbhost,
        'PORT': dbport,
    }
}
