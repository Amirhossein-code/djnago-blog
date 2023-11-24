from dotenv import load_dotenv
from .common import *

load_dotenv()

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME", ""),
        "USER": os.getenv("DB_USER", ""),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", ""),
        "PORT": "3306",
    }
}

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
