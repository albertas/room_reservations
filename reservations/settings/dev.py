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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {"level": "INFO", "class": "logging.StreamHandler", "formatter": "verbose"},
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": str(BASE_DIR / ".." / "info.log"),  # noqa: F405
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
