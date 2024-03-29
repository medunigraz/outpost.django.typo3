import io
import logging

import mimeparse
import requests
from django.http import (
    HttpResponse,
    HttpResponseNotFound,
)
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import View
from PIL import Image

from . import models
from .conf import settings

logger = logging.getLogger(__name__)


@method_decorator(cache_page(3600), name="dispatch")
class MediaView(View):
    def get(self, request, pk, width=None):
        media = get_object_or_404(models.Media, pk=pk)
        timeout = int(settings.TYPO3_MEDIA_CACHE_TIMEOUT.total_seconds())
        response = HttpResponse()
        try:
            req = requests.get(media.url)
            response["Cache-Control"] = f"private,max-age={timeout}"
            contenttype = req.headers.get("Content-Type", "application/octet-stream")
            maintype, *_ = mimeparse.parse_mime_type(contenttype)
            if not width or maintype != "image":
                response["Content-Type"] = contenttype
                response.write(req.content)
                return response
            with Image.open(io.BytesIO(req.content)) as img:
                fmt = img.format
                response["Content-Type"] = Image.MIME[fmt]
                width = int(width)
                if img.width <= width:
                    response.write(req.content)
                    return response
                height = int(img.height * (width / float(img.width)))
                img = img.resize((width, height), Image.ANTIALIAS)
                img.save(
                    response,
                    format=fmt,
                    quality=settings.TYPO3_MEDIA_CACHE_QUALITY,
                    optimize=True,
                )
        except Exception as e:
            logger.warn(f"Failed to load image blob: {e}")
            return HttpResponseNotFound()
        return response
