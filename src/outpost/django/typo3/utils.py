import requests

from memoize import memoize

from .conf import settings


@memoize(timeout=settings.TYPO3_API_CACHE_TIMEOUT.total_seconds())
def fetch(url):
    return requests.get(url, allow_redirects=False)
