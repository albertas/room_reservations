import os

from .base import *  # noqa

INSTALLED_APPS += [  # noqa: F405
    "django_extensions",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "postgres",
        "USER": os.environ.get("DB_PASSWORD", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "postgres"),
        "HOST": "db",
        "PORT": 5432,
    }
}
