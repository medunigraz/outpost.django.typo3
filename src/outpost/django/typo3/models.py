import logging

import requests
from django.conf import settings
from django.contrib.gis.db import models
from memoize import memoize
from purl import URL
from treebeard.al_tree import AL_Node

logger = logging.getLogger(__name__)


@memoize(timeout=600)
def fetch(url):
    return requests.get(url, allow_redirects=False)


class Source(models.Model):
    id = models.PositiveIntegerField(
        primary_key=True
    )
    title = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    private = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'typo3_source'

    def __str__(self):
        return f'{self.title} ({self.pk})'


class DjangoSource(models.Model):
    id = models.OneToOneField(
        'Source',
        models.DO_NOTHING,
        db_constraint=False,
        related_name='+',
        primary_key=True
    )
    private = models.BooleanField(
        default=True
    )

    def __str__(self):
        return str(self.id)


class Language(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `title` (`string`)
    Titel of language.

    ### `flag` (`string`)
    Flag code to be used with icon sets.

    ### `isocode` (`string`)
    [ISO 3361](https://www.iso.org/iso-3166-country-codes.html) code.
    '''
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=256, blank=True, null=True)
    flag = models.CharField(max_length=2, blank=True, null=True)
    isocode = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'typo3_language'

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.title


class Group(models.Model):
    id = models.IntegerField(
        primary_key=True
    )
    title = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'typo3_group'

    class Refresh:
        interval = 3600

    def __str__(self):
        return self.title


class Category(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `language` (`integer`)
    Foreign key to [TYPO3 language](../language).

    ### `title` (`string`)
    Titel of category.

    ### `description` (`string`)
    Full description of category.

    ### `start` (`datetime`)
    Start of period of validity.

    ### `end` (`datetime`)
    End of period of validity.
    '''
    id = models.IntegerField(primary_key=True)
    language = models.ForeignKey(
        'Language',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    marker = models.IntegerField(blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'typo3_category'

    class Refresh:
        interval = 3600

    def __str__(self):
        return self.title


class Calendar(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `title` (`string`)
    Titel of event.

    ### `language` (`integer`)
    Foreign key to [TYPO3 language](../language).

    '''
    id = models.IntegerField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    language = models.ForeignKey(
        'Language',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )

    class Meta:
        managed = False
        db_table = 'typo3_calendar'

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.title


class Media(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.URLField()
    mimetype = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    filename = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    size = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'typo3_media'

    class Refresh:
        interval = 1800

    def __str__(self):
        return self.filename


class EventCategory(AL_Node):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `title` (`string`)
    Titel of event.

    ### `calendar` (`integer`)
    Foreign key to [TYPO3 calendar](../calendar) if this category is only valid
    for a single calendar. A value of `null` indicates a global category.

    ### `parent` (`integer`)
    Foreign key to parent [TYPO3 event category](../eventcategory). A value
    of `null` indicates a root calendar category.

    Only required when assembling the full category
    [AL tree](https://en.wikipedia.org/wiki/Adjacency_list).

    ### `sib_order` (`integer`)
    Value to sort by.

    Only required when assembling the full category
    [AL tree](https://en.wikipedia.org/wiki/Adjacency_list).

    ### `language` (`integer`)
    Foreign key to [TYPO3 language](../language).

    '''
    id = models.IntegerField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    calendar = models.ForeignKey(
        'Calendar',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    parent = models.ForeignKey(
        'self',
        models.SET_NULL,
        related_name='children_set',
        db_constraint=False,
        db_index=False,
        null=True,
        blank=True
    )
    sib_order = models.PositiveIntegerField()
    language = models.ForeignKey(
        'Language',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )

    class Meta:
        managed = False
        db_table = 'typo3_eventcategory'

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.title


class Event(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `start` (`timestamp`)
    Begin of event.

    ### `end` (`timestamp`)
    End of event.

    ### `allday` (`boolean`)
    All-day event.

    ### `title` (`string`)
    Titel of event.

    ### `calendar` (`integer`)
    Foreign key to [TYPO3 calendar](../calendar).

    ### `organizer` (`string`)
    Name of person responsible for event.

    ### `location` (`string`)
    Description of location where event will take place.

    ### `teaser` (`string`)
    Short summary of event description without HTML.

    ### `description` (`string`)
    Full description of event with embedded HTML.

    ### `language` (`integer`)
    Foreign key to [TYPO3 language](../language).

    ### `register` (`boolean`)
    Registration required for event attendance.

    ### `registration_end` (`timestamp`)
    Deadline for event registration.

    ### `attending_fees` (`boolean`)
    Event attendance requires a fee.

    ### `url` (`string`)
    URL where event can be viewed in the frontend CMS.

    ### `dfp_points` (`integer`)
    The amount of [DFP points](https://www.meindfp.at/) credited for
    attendance.

    ### `contact` (`string`)
    The name of a person or party to contact in regards to this event.

    ### `email` (`string`)
    The email address of a person or party to contact in regards to this event.

    ### `last_modified` (`datetime`)
    Date and time of last modification to this event.
    '''
    id = models.IntegerField(primary_key=True)
    source = models.ForeignKey(
        'Source',
        models.DO_NOTHING,
        db_constraint=False,
        related_name='+'
    )
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    allday = models.BooleanField()
    title = models.TextField(blank=True, null=True)
    calendar = models.ForeignKey(
        'Calendar',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    categories = models.ManyToManyField(
        'EventCategory',
        db_table='typo3_event_eventcategory',
        db_constraint=False,
        related_name='+'
    )
    organizer = models.CharField(max_length=256, blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    teaser = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    language = models.ForeignKey(
        'Language',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    register = models.BooleanField()
    registration_end = models.DateTimeField(blank=True, null=True)
    attending_fees = models.BooleanField()
    link = models.CharField(max_length=512, blank=True, null=True)
    dfp_points = models.IntegerField(blank=True, null=True)
    contact = models.CharField(max_length=256, blank=True, null=True)
    email = models.CharField(max_length=256, blank=True, null=True)
    last_modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'typo3_event'
        ordering = (
            'start',
            'end',
        )
        get_latest_by = 'start'

    class Refresh:
        interval = 1800

    @memoize(timeout=3600)
    def url(self):
        url = URL(settings.OUTPOST['typo3_api'])
        url = url.query_param('tx_mugapi_endpoint[recordType]', 'Event')
        url = url.query_param('tx_mugapi_endpoint[recordUid]', self.pk)
        url = url.query_param('tx_mugapi_endpoint[redirect]', 1)
        logger.debug(f'Fetching TYPO3 event URL: {url.as_string()}')
        r = fetch(url.as_string())
        if r.status_code != 302:
            return None
        realurl = URL(r.headers['location'])
        realurl = realurl.fragment('sl-content')
        return realurl.as_string()

    @memoize(timeout=86400)
    def breadcrumb(self):
        url = URL(settings.OUTPOST['typo3_api'])
        url = url.query_param('tx_mugapi_endpoint[recordType]', 'RootLine')
        url = url.query_param('tx_mugapi_endpoint[pageUid]', self.source_id)
        logger.debug(f'Fetching TYPO3 event breadcrumb: {url.as_string()}')
        r = fetch(url.as_string())
        if r.status_code != 200:
            return []
        return list(filter(lambda b: b.get('pid', None) is not None, r.json()))

    def __str__(self):
        return self.title

    def __repr__(self):
        return '{s.__class__.__name__}({s.pk})'.format(s=self)


class EventMedia(models.Model):
    id = models.IntegerField(primary_key=True)
    media = models.ForeignKey(
        'Media',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    event = models.ForeignKey(
        'Event',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='media'
    )
    title = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    alternative = models.TextField(
        blank=True,
        null=True
    )
    language = models.ForeignKey(
        'Language',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    order = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    preview = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'typo3_eventmedia'
        ordering = (
            '-preview',
            '-order',
        )

    class Refresh:
        interval = 1800

    def __str__(s):
        return f'{s.event}: {s.media}'


class NewsCategory(models.Model):
    id = models.CharField(
        max_length=128,
        primary_key=True
    )
    category = models.ForeignKey(
        'Category',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    news = models.ForeignKey(
        'News',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )

    class Meta:
        managed = False
        db_table = 'typo3_newscategory'

    class Refresh:
        interval = 86400

    def __str__(s):
        return f'{s.news.title}: {s.category.title}'


class News(models.Model):
    '''
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `language` (`integer`)
    Foreign key to [TYPO3 language](../language).

    ### `datetime` (`timestamp`)
    Date & time of creation.

    ### `title` (`string`)
    Title of news.

    ### `teaser` (`string`)
    Short summary of news description without HTML.

    ### `body` (`string`)
    Full description of news with embedded HTML.

    ### `start` (`datetime`)
    Begin of validity.

    ### `end` (`datetime`)
    End of validity.

    ### `author` (`string`)
    Full name fo author.

    ### `email` (`string`)
    Email of author.

    ### `keywords` (`string`)
    Comma separated list of keywords.

    ### `tags` (`string`)
    Comma separated list of tags.

    ### `topnews` (`boolean`)
    News are considered top news to be shown on frontpage.

    ### `categories` (`[integer]`)
    List of foreign keys to [TYPO3 categories](../category).

    ### `groups` (`[object]`)
    List of TYPO3 group objects that have been assigned to this news.

    ### `last_modified` (`datetime`)
    Date and time of last modification to this event.
    '''
    id = models.IntegerField(primary_key=True)
    source = models.ForeignKey(
        'Source',
        models.DO_NOTHING,
        db_constraint=False,
        related_name='+'
    )
    language = models.ForeignKey(
        'Language',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    datetime = models.DateTimeField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    teaser = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    tags = models.IntegerField(blank=True, null=True)
    topnews = models.BooleanField()
    categories = models.ManyToManyField(
        'Category',
        through='NewsCategory'
    )
    groups = models.ManyToManyField(
        'Group',
        db_table='typo3_news_group',
        db_constraint=False,
        related_name='+'
    )
    last_modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'typo3_news'
        ordering = (
            '-datetime',
        )
        get_latest_by = 'datetime'

    class Refresh:
        interval = 1800

    @memoize(timeout=3600)
    def url(self):
        url = URL(settings.OUTPOST['typo3_api'])
        url = url.query_param('tx_mugapi_endpoint[recordType]', 'News')
        url = url.query_param('tx_mugapi_endpoint[recordUid]', self.pk)
        url = url.query_param('tx_mugapi_endpoint[redirect]', 1)
        url = url.fragment('sl-content')
        logger.debug(f'Fetching TYPO3 news URL: {url.as_string()}')
        r = fetch(url.as_string())
        if r.status_code != 302:
            return None
        realurl = URL(r.headers['location'])
        realurl = realurl.fragment('sl-content')
        return realurl.as_string()

    @memoize(timeout=86400)
    def breadcrumb(self):
        url = URL(settings.OUTPOST['typo3_api'])
        url = url.query_param('tx_mugapi_endpoint[recordType]', 'RootLine')
        url = url.query_param('tx_mugapi_endpoint[pageUid]', self.source_id)
        logger.debug(f'Fetching TYPO3 news breadcrumb: {url.as_string()}')
        r = fetch(url.as_string())
        if r.status_code != 200:
            return []
        return list(filter(lambda b: b.get('pid', None) is not None, r.json()))

    def __str__(self):
        return self.title

    def __repr__(self):
        return '{s.__class__.__name__}({s.pk})'.format(s=self)


class NewsMedia(models.Model):
    id = models.IntegerField(primary_key=True)
    media = models.ForeignKey(
        'Media',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    news = models.ForeignKey(
        'News',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='media'
    )
    title = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    alternative = models.TextField(
        blank=True,
        null=True
    )
    language = models.ForeignKey(
        'Language',
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name='+'
    )
    order = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    preview = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'typo3_newsmedia'
        ordering = (
            '-preview',
            '-order',
        )

    class Refresh:
        interval = 1800

    def __str__(s):
        return f'{s.news}: {s.media}'
