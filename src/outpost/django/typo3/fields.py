import re

from django.db import models
from bs4 import BeautifulSoup
from purl import URL

from .conf import settings


class RichTextField(models.TextField):

    fileadmin = URL(settings.TYPO3_FILEADMIN_URL)

    regex = (
        (
            r'<a href="mailto:\g<mail>" title="\g<title>">\g<content></a>',
            re.compile(
                r"""<link\s(?P<mail>[\w\.\+\-]+@(?:[\w]+\.)+[a-z]+)(?:\s+"(?P<title>[^>]*)")?>(?P<content>.+?)<\/link>"""
            ),
        ),
        (
            r'<a file="\g<id>" target="\g<target>" title="\g<title>">\g<content></a>',
            re.compile(
                r"<link\sfile:(?P<id>\d+)(?:\s(?P<target>.*?)?(?:\s\"(?P<title>.*?)\")?)?>(?P<content>.+?)<\/link>"
            ),
        ),
        (
            r'<a href="\g<url>" target="\g<target>" title="\g<title>">\g<content></a>',
            re.compile(
                r"<link\s(?P<url>https?:\/\/.+?)(?:\s(?P<target>.*?)?(?:\s\"(?P<title>.*?)\")?)?>(?P<content>.+?)<\/link>"
            ),
        ),
        (
            r'<a path="\g<path>" target="\g<target>" title="\g<title>">\g<content></a>',
            re.compile(
                r"<link\s(?P<path>(?!file:|https?:).+?)(?:\s(?P<target>.*?)?(?:\s\"(?P<title>.*?)\")?)?>(?P<content>.+?)<\/link>"
            ),
        ),
    )
    parser = {
        "a": ("link_file", "link_path", "a_file"),
        "img": ("images_data", "images_src", "clean_attrs_data"),
        None: ("clean_attrs_empty",),
    }
    functions = ("paragraphs",)

    def __init__(self, media_model, *args, **kwargs):
        self.media_model = media_model
        super().__init__(*args, **kwargs)

    def function_paragraphs(self, html):
        parts = re.split(r"\r?\n", html)
        body = "</p><p>".join(parts[1:])
        return f"{parts[0]}<p>{body}</p>"

    def handle_link_file(self, elem):
        pk = elem.attrs.pop("file", None)
        if not pk:
            return
        try:
            media = models.Media.objects.get(pk=int(pk))
            elem.attrs["href"] = media.url
        except models.Media.DoesNotExist:
            return

    def handle_link_path(self, elem):
        path = elem.attrs.pop("path", None)
        if not path:
            return
        elem.attrs["href"] = self.fileadmin.path(path).as_string()

    def handle_a_file(self, elem):
        if "href" not in elem.attrs:
            return
        url = URL(elem.attrs["href"])
        if url.scheme() != "t3":
            return
        if url.host() != "file":
            return
        if not url.has_query_param("uid"):
            return
        try:
            media = self.media_model.objects.get(pk=url.query_param("uid"))
        except self.media_model.DoesNotExist:
            return
        base = URL(media.storage.url)
        elem.attrs["href"] = base.path_segments(
            URL(media.url).path_segments()
        ).as_string()

    def handle_images_data(self, elem):
        if elem.attrs.get("data-htmlarea-file-table") != "sys_file":
            return
        if "data-htmlarea-file-uid" not in elem.attrs:
            return
        try:
            pk = elem.attrs.get("data-htmlarea-file-uid")
            media = models.Media.objects.get(pk=pk)
            elem.attrs["src"] = media.url
        except models.Media.DoesNotExist:
            return

    def handle_images_src(self, elem):
        url = URL(elem.attrs.get("src"))
        if url.path().startswith("fileadmin"):
            elem.attrs["src"] = self.fileadmin.path(url.path()).as_string()

    def handle_clean_attrs_data(self, elem):
        elem.attrs = {k: v for k, v in elem.attrs.items() if not k.startswith("data-")}

    def handle_clean_attrs_empty(self, elem):
        elem.attrs = {k: v for k, v in elem.attrs.items() if v}

    def from_db_value(self, value, expression, connection, context):
        for name in self.functions:
            func = getattr(self, f"function_{name}", None)
            if func:
                value = func(value)
        for (replacement, pattern) in self.regex:
            value = pattern.sub(replacement, value)
        parsed = BeautifulSoup(value, "html.parser")
        for query, handlers in self.parser.items():
            for elem in parsed.find_all(query):
                for handler in handlers:
                    func = getattr(self, f"handle_{handler}", None)
                    if func:
                        func(elem)
        return str(parsed)