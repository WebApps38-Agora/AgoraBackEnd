from ._base import *

SECRET_KEY = os.environ['DJANGO_KEY']
DEBUG = False

ALLOWED_HOSTS = [
    os.environ['HOST_IP'],
    os.environ['HOST_URL'],
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['PGDATABASE'],
        'USER': os.environ['PGUSER'],
        'PASSWORD': os.environ['PGPASSWORD'],
        'HOST': os.environ['PGHOST'],
        'PORT': os.environ['PGPORT'],
    },
}
