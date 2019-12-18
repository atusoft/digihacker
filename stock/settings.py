# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sqlite.db',
    }
}

INSTALLED_APPS = (
    'data',
    )

SECRET_KEY = 'REPLACE_ME'