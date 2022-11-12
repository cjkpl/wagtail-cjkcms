# boot_django.py
#
# This file sets up and configures Django. It's used by scripts that need to
# execute as if running in a Django server.
import os
import django
from django.conf import settings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "cjkcms"))
BASE_URL = "http://localhost"


def boot_django():
    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
            }
        },
        INSTALLED_APPS=(
            # --- wagtail-cjkcms #
            "cjkcms",
            # --- wagtail-cjkcms requirements #
            "wagtailseo",
            "wagtailcache",
            "wagtail.contrib.table_block",
            "wagtail.contrib.settings",
            "wagtail.contrib.modeladmin",
            "django_bootstrap5",
            # --- end wagtail-cjkcms #
            # "wagtail.contrib.forms",
            # "wagtail.contrib.redirects",
            "wagtail.sites",
            "wagtail.admin",
            "wagtail.snippets",
            "wagtail.documents",
            "wagtail.images",
            "wagtail.search",
            "wagtail",
            "wagtail.contrib.sitemaps",
            "django.contrib.sitemaps",
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.messages",
            "django.contrib.sessions",
            "taggit",
        ),
        TIME_ZONE="UTC",
        USE_TZ=True,
        MIDDLEWARE=[
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
        ],
        SECRET_KEY="not-important",
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [
                    os.path.join(BASE_DIR, "templates"),
                ],
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.debug",
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    ],
                },
            },
        ],
        WAGTAILADMIN_BASE_URL=BASE_URL,
        BASE_URL=BASE_URL,
        ROOT_URLCONF="boot_urls",
    )
    django.setup()
