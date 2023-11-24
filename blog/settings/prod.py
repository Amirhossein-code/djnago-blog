from .common import *

SECRET_KEY = "%na*knyglp1q^(7xz_r*d6)iz9n)ocy=ko(_a5xip5jg*#^trhb-$*tk+fefps@kqa*e0c-0papxe%jzcvs7d@yij1jz1sc3cmqd"

DEBUG = True

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "debug_toolbar",
    "django_filters",
    "rest_framework",
    "djoser",
    "taggit",
]

LOCAL_APPS = [
    "app",
    "posts",
    "categories",
    "search",
    "review",
    "core",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "blog",
        "USER": "root",
        "PASSWORD": "MySQL124@SE",
        "HOST": "localhost",
        "PORT": 3306,
    }
}

ALLOWED_HOSTS = []
