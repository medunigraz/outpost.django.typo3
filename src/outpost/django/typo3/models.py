import logging
from functools import reduce

from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from memoize import memoize
from ordered_model.models import OrderedModel
from phonenumber_field.modelfields import PhoneNumberField
from purl import URL

from .conf import settings
from .fields import (
    LinkField,
    RichTextField,
)
from .utils import fetch

logger = logging.getLogger(__name__)


class Source(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=256, blank=True, null=True)
    private = models.BooleanField()

    class Meta:
        managed = False
        db_table = "typo3_source"

    def __str__(self):
        return f"{self.title} ({self.pk})"


class DjangoSource(models.Model):
    id = models.OneToOneField(
        "Source",
        models.DO_NOTHING,
        db_constraint=False,
        related_name="+",
        primary_key=True,
    )
    private = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)


class Storage(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=256, blank=True, null=True)
    url = models.URLField()

    class Meta:
        managed = False
        db_table = "typo3_storage"

    def __str__(self):
        return f"{self.title} ({self.pk})"


class DjangoStorage(models.Model):
    id = models.OneToOneField(
        "Storage",
        models.DO_NOTHING,
        db_constraint=False,
        related_name="+",
        primary_key=True,
    )
    url = models.URLField()

    def __str__(self):
        return str(self.id)


class Language(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `title` (`string`)
    Titel of language.

    ### `flag` (`string`)
    [ISO 3361-1](https://en.wikipedia.org/wiki/ISO_3166-1) code.

    ### `isocode` (`string`)
    [ISO 639-1](https://en.wikipedia.org/wiki/ISO_639-1) code.
    """

    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=256, blank=True, null=True)
    flag = models.CharField(max_length=2, blank=True, null=True)
    isocode = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "typo3_language"

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.title


class Group(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `title` (`string`)
    Titel of group.
    """

    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "typo3_group"

    class Refresh:
        interval = 3600

    def __str__(self):
        return self.title


class Category(models.Model):
    """
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
    """

    id = models.IntegerField(primary_key=True)
    language = models.ForeignKey(
        "Language",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    marker = models.IntegerField(blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "typo3_category"

    class Refresh:
        interval = 3600

    def __str__(self):
        return self.title


class Media(models.Model):
    id = models.IntegerField(primary_key=True)
    storage = models.ForeignKey(
        "Storage",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    path = models.TextField()
    mimetype = models.CharField(max_length=256, blank=True, null=True)
    filename = models.CharField(max_length=256, blank=True, null=True)
    size = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "typo3_media"

    class Refresh:
        interval = 1800

    @property
    def url(self):
        return reduce(
            lambda u, p: u.add_path_segment(p),
            URL(self.path).path_segments(),
            URL(self.storage.url),
        ).as_string()

    def __str__(self):
        return self.filename


class EventCategory(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    category = models.ForeignKey(
        "Category",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    event = models.ForeignKey(
        "Event",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )

    class Meta:
        managed = False
        db_table = "typo3_eventcategory"

    def __str__(s):
        return f"{s.event.title}: {s.category.title}"


class Event(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `url` (`string`)
    URL pointing to the original location of this event object.

    ### `media` (`[object]`)
    List of associated media objects.

    ### `breadcrumb` (`[object]`)
    List of nodes in the page tree where this news objects is located.

    ### `categories` (`[integer]`)
    List of foreign keys to [TYPO3 categories](../category).

    ### `groups` (`[object]`)
    List of foreign keys to [TYPO3 groups](../group).

    ### `body` (`string`)
    Full description of news with embedded HTML.

    ### `link` (`string`)
    URL pointing to the an external site related to this event.

    ### `start` (`timestamp`)
    Begin of event.

    ### `end` (`timestamp`)
    End of event.

    ### `allday` (`boolean`)
    All-day event.

    ### `title` (`string`)
    Titel of event.

    ### `organizer` (`string`)
    Name of person responsible for event.

    ### `location` (`string`)
    Description of location where event will take place.

    ### `teaser` (`string`)
    Short summary of event description without HTML.

    ### `register` (`boolean`)
    Registration required for event attendance.

    ### `registration_end` (`timestamp`)
    Deadline for event registration.

    ### `attending_fees` (`boolean`)
    Event attendance requires a fee.

    ### `attending_fees_info` (`string`)
    Informative text about detailing attendance fees.

    ### `dfp_points` (`integer`)
    The amount of [DFP points](https://www.meindfp.at/) credited for
    attendance.

    ### `contact` (`string`)
    The name of a person or party to contact in regards to this event.

    ### `email` (`string`)
    The email address of a person or party to contact in regards to this event.

    ### `last_modified` (`datetime`)
    Date and time of last modification to this event.

    ### `language` (`integer`)
    Foreign key to [TYPO3 language](../language).
    """

    id = models.IntegerField(primary_key=True)
    source = models.ForeignKey(
        "Source", models.DO_NOTHING, db_constraint=False, related_name="+"
    )
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    allday = models.BooleanField()
    title = models.TextField(blank=True, null=True)
    categories = models.ManyToManyField("Category", through="EventCategory")
    organizer = models.CharField(max_length=256, blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    teaser = models.TextField(blank=True, null=True)
    body = RichTextField(Media, blank=True, null=True)
    keywords = ArrayField(
        models.TextField(blank=True),
    )
    description = models.TextField(blank=True, null=True)
    language = models.ForeignKey(
        "Language",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    register = models.BooleanField()
    registration_end = models.DateTimeField(blank=True, null=True)
    attending_fees = models.BooleanField()
    attending_fees_info = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=512, blank=True, null=True)
    dfp_points = models.IntegerField(blank=True, null=True)
    contact = models.CharField(max_length=256, blank=True, null=True)
    email = models.CharField(max_length=256, blank=True, null=True)
    last_modified = models.DateTimeField(blank=True, null=True)
    groups = models.ManyToManyField(
        "Group",
        db_table="typo3_event_group",
        db_constraint=False,
        related_name="events",
    )
    header_image = models.ForeignKey(
        "Media",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )

    class Meta:
        managed = False
        db_table = "typo3_event"
        ordering = ("-start", "-end")
        get_latest_by = "start"

    class Refresh:
        interval = 1800

    @memoize(timeout=3600)
    def url(self):
        url = URL(settings.TYPO3_API_URL)
        url = url.query_param("tx_mugapi_endpoint[recordType]", "Event")
        url = url.query_param("tx_mugapi_endpoint[recordUid]", self.pk)
        url = url.query_param("tx_mugapi_endpoint[redirect]", 1)
        logger.debug(f"Fetching TYPO3 event URL: {url.as_string()}")
        r = fetch(url.as_string())
        if r.status_code != 302:
            return None
        realurl = URL(r.headers["location"])
        realurl = realurl.fragment("sl-content")
        return realurl.as_string()

    @memoize(timeout=86400)
    def breadcrumb(self):
        url = URL(settings.TYPO3_API_URL)
        url = url.query_param("tx_mugapi_endpoint[recordType]", "RootLine")
        url = url.query_param("tx_mugapi_endpoint[pageUid]", self.source_id)
        logger.debug(f"Fetching TYPO3 event breadcrumb: {url.as_string()}")
        r = fetch(url.as_string())
        if r.status_code != 200:
            return []
        return list(filter(lambda b: b.get("pid", None) is not None, r.json()))

    def __str__(self):
        return f"{self.start} - {self.end}: {self.title}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.pk})"


class EventMedia(models.Model):
    id = models.IntegerField(primary_key=True)
    media = models.ForeignKey(
        "Media",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    event = models.ForeignKey(
        "Event",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="media",
    )
    title = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    alternative = models.TextField(blank=True, null=True)
    language = models.ForeignKey(
        "Language",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    order = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "typo3_eventmedia"
        ordering = ("-order",)

    class Refresh:
        interval = 1800

    def __str__(s):
        return f"{s.event}: {s.media}"


class EventGallery(models.Model):
    id = models.IntegerField(primary_key=True)
    media = models.ForeignKey(
        "Media",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    event = models.ForeignKey(
        "Event",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="gallery",
    )
    title = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    alternative = models.TextField(blank=True, null=True)
    language = models.ForeignKey(
        "Language",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    order = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "typo3_eventgallery"
        ordering = ("-order",)

    class Refresh:
        interval = 1800

    def __str__(s):
        return f"{s.event}: {s.media}"


class EventContactBox(models.Model):
    id = models.IntegerField(primary_key=True)
    media = models.ForeignKey(
        "Media",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    event = models.ForeignKey(
        "Event",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="contact_box",
    )
    title = models.CharField(max_length=256, blank=True, null=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    link_label = models.CharField(max_length=256, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    headline = models.CharField(max_length=256, blank=True, null=True)
    address = ArrayField(models.CharField(max_length=256, blank=True, null=True))

    class Meta:
        managed = False
        db_table = "typo3_eventcontactbox"

    class Refresh:
        interval = 1800

    def __str__(s):
        return f"{s.event}: {s.media}"


class NewsCategory(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    category = models.ForeignKey(
        "Category",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    news = models.ForeignKey(
        "News",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )

    class Meta:
        managed = False
        db_table = "typo3_newscategory"

    class Refresh:
        interval = 86400

    def __str__(s):
        return f"{s.news.title}: {s.category.title}"


class News(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `url` (`string`)
    URL pointing to the original location of this news object.

    ### `media` (`[object]`)
    List of associated media objects.

    ### `breadcrumb` (`[object]`)
    List of nodes in the page tree where this news objects is located.

    ### `categories` (`[integer]`)
    List of foreign keys to [TYPO3 categories](../category).

    ### `groups` (`[object]`)
    List of foreign keys to [TYPO3 groups](../group).

    ### `body` (`string`)
    Full description of news with embedded HTML.

    ### `datetime` (`timestamp`)
    Date & time of creation.

    ### `title` (`string`)
    Title of news.

    ### `teaser` (`string`)
    Short summary of news description without HTML.

    ### `start` (`datetime`)
    Begin of validity.

    ### `end` (`datetime`)
    End of validity.

    ### `author` (`string`)
    Full name fo author.

    ### `email` (`string`)
    Email of author.

    ### `keywords` (`string[]`)
    List of metadata keywords.

    ### `description` (`string`)
    Metadata description text.

    ### `topnews` (`boolean`)
    News are considered top news to be shown on frontpage.

    ### `last_modified` (`datetime`)
    Date and time of last modification to this event.

    ### `language` (`integer`)
    Foreign key to [TYPO3 language](../language).
    """

    id = models.IntegerField(primary_key=True)
    source = models.ForeignKey(
        "Source", models.DO_NOTHING, db_constraint=False, related_name="+"
    )
    language = models.ForeignKey(
        "Language",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    datetime = models.DateTimeField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    teaser = models.TextField(blank=True, null=True)
    body = RichTextField(Media, blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    keywords = ArrayField(
        models.TextField(blank=True),
    )
    description = models.TextField(blank=True, null=True)
    tags = models.IntegerField(blank=True, null=True)
    topnews = models.BooleanField()
    categories = models.ManyToManyField("Category", through="NewsCategory")
    groups = models.ManyToManyField(
        "Group", db_table="typo3_news_group", db_constraint=False, related_name="news"
    )
    last_modified = models.DateTimeField(blank=True, null=True)
    header_image = models.ForeignKey(
        "Media",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )

    class Meta:
        managed = False
        db_table = "typo3_news"
        ordering = ("-datetime",)
        get_latest_by = "datetime"

    class Refresh:
        interval = 1800

    @memoize(timeout=3600)
    def url(self):
        url = URL(settings.TYPO3_API_URL)
        url = url.query_param("tx_mugapi_endpoint[recordType]", "News")
        url = url.query_param("tx_mugapi_endpoint[recordUid]", self.pk)
        url = url.query_param("tx_mugapi_endpoint[redirect]", 1)
        url = url.fragment("sl-content")
        logger.debug(f"Fetching TYPO3 news URL: {url.as_string()}")
        r = fetch(url.as_string())
        if r.status_code != 302:
            return None
        realurl = URL(r.headers["location"])
        realurl = realurl.fragment("sl-content")
        return realurl.as_string()

    @memoize(timeout=86400)
    def breadcrumb(self):
        url = URL(settings.TYPO3_API_URL)
        url = url.query_param("tx_mugapi_endpoint[recordType]", "RootLine")
        url = url.query_param("tx_mugapi_endpoint[pageUid]", self.source_id)
        logger.debug(f"Fetching TYPO3 news breadcrumb: {url.as_string()}")
        r = fetch(url.as_string())
        if r.status_code != 200:
            return []
        return list(filter(lambda b: b.get("pid", None) is not None, r.json()))

    def __str__(self):
        return f"{self.datetime}: {self.title}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.pk})"


class NewsMedia(models.Model):
    id = models.IntegerField(primary_key=True)
    media = models.ForeignKey(
        "Media",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    news = models.ForeignKey(
        "News",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="media",
    )
    title = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    alternative = models.TextField(blank=True, null=True)
    language = models.ForeignKey(
        "Language",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    order = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "typo3_newsmedia"
        ordering = ("-order",)

    class Refresh:
        interval = 1800

    def __str__(s):
        return f"{s.news}: {s.media}"


class NewsGallery(models.Model):
    id = models.IntegerField(primary_key=True)
    media = models.ForeignKey(
        "Media",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    news = models.ForeignKey(
        "News",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="gallery",
    )
    title = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    alternative = models.TextField(blank=True, null=True)
    language = models.ForeignKey(
        "Language",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    order = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "typo3_newsgallery"
        ordering = ("-order",)

    class Refresh:
        interval = 1800

    def __str__(s):
        return f"{s.news}: {s.media}"


class NewsContactBox(models.Model):
    id = models.IntegerField(primary_key=True)
    media = models.ForeignKey(
        "Media",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    news = models.ForeignKey(
        "News",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="contact_box",
    )
    title = models.CharField(max_length=256, blank=True, null=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    link_label = models.CharField(max_length=256, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    headline = models.CharField(max_length=256, blank=True, null=True)
    address = ArrayField(models.CharField(max_length=256, blank=True, null=True))

    class Meta:
        managed = False
        db_table = "typo3_newscontactbox"

    class Refresh:
        interval = 1800

    def __str__(s):
        return f"{s.news}: {s.media}"


class NewsRelatedLink(OrderedModel):
    source = models.ForeignKey(
        "Source", models.DO_NOTHING, db_constraint=False, related_name="+"
    )
    language = models.ForeignKey(
        "Language",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    datetime = models.DateTimeField(blank=True, null=True)
    news = models.ForeignKey(
        "News",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="related_links",
    )
    title = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = LinkField(Media)

    class Meta:
        managed = False
        db_table = "typo3_news_related_link"

    class Refresh:
        interval = 1800

    def __str__(s):
        return f"{s.news}: {s.title}"


class NewsRelatedMedia(OrderedModel):
    source = models.ForeignKey(
        "Source", models.DO_NOTHING, db_constraint=False, related_name="+"
    )
    language = models.ForeignKey(
        "Language",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    datetime = models.DateTimeField(blank=True, null=True)
    news = models.ForeignKey(
        "News",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="related_media",
    )
    title = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    media = models.ForeignKey(
        "Media",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )

    class Meta:
        managed = False
        db_table = "typo3_news_related_media"

    class Refresh:
        interval = 1800

    def __str__(s):
        return f"{s.news}: {s.title}"


class ZMFCourse(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `last_modified` (`datetime`)
    Date and time of last modification to this ZMF course.

    ### ` created` (`datetime`)
    Date and time of creation of this ZMF course.

    ### `title` (`string`)
    Titel of category.

    ### `description` (`string`)
    Full description of this ZMF course.

    ### `email` (`string`)
    Contact email address.

    ### `language` (`integer`)
    Foreign key to [TYPO3 language](../language).

    ### `category` (`integer`)
    Foreign key to [TYPO3 category](../category).
    """

    id = models.IntegerField(primary_key=True)
    page = models.IntegerField()
    last_modified = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    language = models.ForeignKey(
        "Language",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    category = models.ForeignKey(
        "Category",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )

    class Meta:
        managed = False
        db_table = "typo3_zmf_course"

    def __str__(self):
        return self.title
