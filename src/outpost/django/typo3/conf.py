from datetime import timedelta
from appconf import AppConf
from django.conf import settings


class Typo3AppConf(AppConf):
    API_URL = "http://localhost/api/"
    MEDIA_CACHE_TIMEOUT = timedelta(days=14)
    MEDIA_CACHE_QUALITY = 95

    class Meta:
        prefix = "typo3"
