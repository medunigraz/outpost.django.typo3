import logging
import re

from bs4 import BeautifulSoup
from django.conf import settings
from django.urls import reverse
from drf_haystack.serializers import HaystackSerializerMixin
from memoize import memoize
from purl import URL
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework.serializers import (
    Field,
    ModelSerializer,
    PrimaryKeyRelatedField,
    ReadOnlyField,
    SerializerMethodField,
    URLField,
)

from . import models

logger = logging.getLogger(__name__)


class RichTextField(Field):

    fileadmin = URL(settings.OUTPOST.get('typo3_fileadmin'))

    regex = (
        (
            r'<a href="mailto:\g<mail>">\g<content></a>',
            re.compile(r'<link\s(?P<mail>[\w\.\+\-]+\@(?:[\w]+\.)+[a-z]+)>(?P<content>.+?)<\/link>'),
        ),
        (
            r'<a file="\g<id>" target="\g<target>" title="\g<title>">\g<content></a>',
            re.compile(r'<link\sfile:(?P<id>\d+)(?:\s(?P<target>.*?)?(?:\s\"(?P<title>.*?)\")?)?>(?P<content>.+?)<\/link>'),
        ),
        (
            r'<a href="\g<url>" target="\g<target>" title="\g<title>">\g<content></a>',
            re.compile(r'<link\s(?P<url>https?:\/\/.+?)(?:\s(?P<target>.*?)?(?:\s\"(?P<title>.*?)\")?)?>(?P<content>.+?)<\/link>'),
        ),
        (
            r'<a path="\g<path>" target="\g<target>" title="\g<title>">\g<content></a>',
            re.compile(r'<link\s(?P<path>(?!file:|https?:).+?)(?:\s(?P<target>.*?)?(?:\s\"(?P<title>.*?)\")?)?>(?P<content>.+?)<\/link>'),
        ),
    )
    parser = {
        'a': (
            'link_file',
            'link_path',
        ),
        'img': (
            'images_data',
            'images_src',
            'clean_attrs_data',
        ),
        None: (
            'clean_attrs_empty',
        ),
    }
    functions = (
        'paragraphs',
    )

    def function_paragraphs(self, html):
        parts = re.split(r'\r?\n', html)
        body = '</p><p>'.join(parts[1:])
        return f'{parts[0]}<p>{body}</p>'

    def handle_link_file(self, elem):
        pk = elem.attrs.pop('file', None)
        if not pk:
            return
        try:
            media = models.Media.objects.get(pk=int(pk))
            elem.attrs['href'] = media.url
        except models.Media.DoesNotExist:
            return

    def handle_link_path(self, elem):
        path = elem.attrs.pop('path', None)
        if not path:
            return
        elem.attrs['href'] = self.fileadmin.path(path).as_string()

    def handle_images_data(self, elem):
        if elem.attrs.get('data-htmlarea-file-table') != 'sys_file':
            return
        if 'data-htmlarea-file-uid' not in elem.attrs:
            return
        try:
            pk = elem.attrs.get('data-htmlarea-file-uid')
            media = models.Media.objects.get(pk=pk)
            elem.attrs['src'] = media.url
        except models.Media.DoesNotExist:
            return

    def handle_images_src(self, elem):
        url = URL(elem.attrs.get('src'))
        if url.path().startswith('fileadmin'):
            elem.attrs['src'] = self.fileadmin.path(url.path()).as_string()

    def handle_clean_attrs_data(self, elem):
        elem.attrs = {k: v for k, v in elem.attrs.items() if not k.startswith('data-')}

    def handle_clean_attrs_empty(self, elem):
        elem.attrs = {k: v for k, v in elem.attrs.items() if v}

    @memoize(timeout=3600)
    def to_representation(self, body):
        html = body
        for name in self.functions:
            func = getattr(self, f'function_{name}', None)
            if func:
                html = func(html)
        for (replacement, pattern) in self.regex:
            html = pattern.sub(replacement, html)
        parsed = BeautifulSoup(html, 'html.parser')
        for query, handlers in self.parser.items():
            for elem in parsed.find_all(query):
                for handler in handlers:
                    func = getattr(self, f'handle_{handler}', None)
                    if func:
                        func(elem)
        return str(parsed)


class LanguageSerializer(ModelSerializer):
    class Meta:
        model = models.Language
        fields = '__all__'


class GroupSerializer(ModelSerializer):

    class Meta:
        model = models.Group
        fields = '__all__'


class CategorySerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `language`

    '''
    expandable_fields = {
        'language': (
            LanguageSerializer,
            {
                'source': 'language',
            }
        ),
    }

    class Meta:
        model = models.Category
        exclude = (
            'marker',
        )


class CalendarSerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `language`

    '''
    expandable_fields = {
        'language': (
            LanguageSerializer,
            {
                'source': 'language',
            }
        ),
    }

    class Meta:
        model = models.Calendar
        fields = '__all__'


class MediaSerializer(FlexFieldsModelSerializer):
    url = SerializerMethodField()
    original = URLField(source='url')

    class Meta:
        model = models.Media
        fields = '__all__'

    def get_url(self, obj):
        path = reverse('typo3:media', kwargs={'pk': obj.pk})
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(path)
        return path


class EventMediaSerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `language`

    '''
    media = MediaSerializer(read_only=True)
    expandable_fields = {
        'language': (
            LanguageSerializer,
            {
                'source': 'language',
            }
        ),
    }

    class Meta:
        model = models.EventMedia
        exclude = (
            'order',
            'event',
        )


class EventCategorySerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `calendar`
     * `language`

    '''
    expandable_fields = {
        'calendar': (
            CalendarSerializer,
            {
                'source': 'calendar',
            }
        ),
        'language': (
            LanguageSerializer,
            {
                'source': 'language',
            }
        ),
    }

    class Meta:
        model = models.EventCategory
        fields = '__all__'


class EventSerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `calendar`
     * `language`

    '''
    expandable_fields = {
        'calendar': (
            CalendarSerializer,
            {
                'source': 'calendar',
            }
        ),
        'language': (
            LanguageSerializer,
            {
                'source': 'language',
            }
        ),
    }
    media = EventMediaSerializer(many=True, read_only=True)
    breadcrumb = ReadOnlyField()
    url = URLField(read_only=True, allow_null=True)
    link = URLField(read_only=True, allow_null=True)
    description = RichTextField(read_only=True)

    class Meta:
        model = models.Event
        exclude = (
            'source',
        )


class EventSearchSerializer(HaystackSerializerMixin, EventSerializer):
    url = URLField(read_only=True, allow_null=True)

    class Meta(EventSerializer.Meta):
        field_aliases = None
        search_fields = (
            'text',
        )


class NewsMediaSerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `language`

    '''
    media = MediaSerializer(read_only=True)
    expandable_fields = {
        'language': (
            LanguageSerializer,
            {
                'source': 'language',
            }
        ),
    }

    class Meta:
        model = models.NewsMedia
        exclude = (
            'order',
            'news',
        )


class NewsSerializer(FlexFieldsModelSerializer):
    '''
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `categories`
     * `language`

    '''
    expandable_fields = {
        'categories': (
            CategorySerializer,
            {
                'source': 'categories',
                'many': True,
            }
        ),
        'language': (
            LanguageSerializer,
            {
                'source': 'language',
            }
        ),
    }
    url = URLField(read_only=True, allow_null=True)
    media = NewsMediaSerializer(many=True, read_only=True)
    breadcrumb = ReadOnlyField()
    categories = PrimaryKeyRelatedField(many=True, read_only=True)
    groups = GroupSerializer(many=True, read_only=True)
    body = RichTextField()

    class Meta:
        model = models.News
        exclude = (
            'source',
            'tags',
        )


class NewsSearchSerializer(HaystackSerializerMixin, NewsSerializer):
    url = URLField(read_only=True, allow_null=True)

    class Meta(NewsSerializer.Meta):
        field_aliases = None
        search_fields = (
            'text',
        )
