from appconf import AppConf
from django.conf import settings


class Typo3AppConf(AppConf):
    API_URL = "https://www.medunigraz.at/api/"
    FILEADMIN_URL = "https://www.medunigraz.at/fileadmin"

    class Meta:
        prefix = "typo3"
