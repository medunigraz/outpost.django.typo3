from datetime import timedelta

from appconf import AppConf
from django.conf import settings


class Typo3AppConf(AppConf):
    API_URL = "http://localhost/api/"
    API_CACHE_TIMEOUT = timedelta(minutes=30)
    PAGE_URL = "http://localhost/index.php"
    MEDIA_CACHE_TIMEOUT = timedelta(days=14)
    MEDIA_CACHE_QUALITY = 95

    class Meta:
        prefix = "typo3"
