from appconf import AppConf
from django.conf import settings


class Typo3AppConf(AppConf):
    API_URL = "http://localhost/api/"
    FILEADMIN_URL = "http://localhost/fileadmin"

    class Meta:
        prefix = "typo3"
