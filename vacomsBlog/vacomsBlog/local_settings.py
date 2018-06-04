DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vacomsDB',
        'USER': 'root',
        'PASSWORD': 'bogdan1994',
        'HOST': '',
        'PORT': '',
    }
}

FRONT_HOST = 'localhost:8000'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'dubas.writer@gmail.com'
EMAIL_HOST_PASSWORD = 'bogdan1994'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'dubas.writer@gmail.com'
