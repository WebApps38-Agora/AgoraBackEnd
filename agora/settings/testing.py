from ._base import *

SECRET_KEY = 'ccpyso^z!(fa^5@rgj#8f4-dp=^*fv7)juf%k^!d=u@*68+2d3'
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}
