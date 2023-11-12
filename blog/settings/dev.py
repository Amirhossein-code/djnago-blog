from .common import *

DEBUG = True

SECRET_KEY = "%na*knyglp1q^(7xz_r*d6)iz9n)ocy=ko(_a5xip5jg*#^trhb-$*tk+fefps@kqa*e0c-0papxe%jzcvs7d@yij1jz1sc3cmqd"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "blog",
        "HOST": "localhost",
        "USER": "root",
        "PASSWORD": "MySQL124@SE",
    }
}
