

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'feedbacks',  # Database name
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': 5432
    }
}

INSTALLED_APPS = (
    'data',
)

SECRET_KEY = 'SECRET_KEY'
