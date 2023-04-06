import logging

from django.urls import reverse
from drf_haystack.serializers import HaystackSerializerMixin
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


class LanguageSerializer(ModelSerializer):
    class Meta:
        model = models.Language
        fields = "__all__"


class GroupSerializer(ModelSerializer):
    """"""

    class Meta:
        model = models.Group
        fields = "__all__"


class CategorySerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `language`

    """

    expandable_fields = {"language": (LanguageSerializer, {"source": "language"})}

    class Meta:
        model = models.Category
        exclude = ("marker",)


class MediaSerializer(FlexFieldsModelSerializer):
    url = SerializerMethodField()
    original = URLField(source="url")

    class Meta:
        model = models.Media
        fields = ("url", "original", "mimetype", "filename", "size")

    def get_url(self, obj):
        path = reverse("typo3:media", kwargs={"pk": obj.pk})
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(path)
        return path


class EventMediaSerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `language`

    """

    media = MediaSerializer(read_only=True)
    expandable_fields = {"language": (LanguageSerializer, {"source": "language"})}

    class Meta:
        model = models.EventMedia
        exclude = ("order", "event")


class EventCategorySerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `language`

    """

    expandable_fields = {"language": (LanguageSerializer, {"source": "language"})}

    class Meta:
        model = models.EventCategory
        fields = "__all__"


class EventSerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `language`

    """

    expandable_fields = {
        "categories": (CategorySerializer, {"source": "categories", "many": True}),
        "language": (LanguageSerializer, {"source": "language"}),
    }
    url = URLField(read_only=True, allow_null=True)
    media = EventMediaSerializer(many=True, read_only=True)
    breadcrumb = ReadOnlyField()
    categories = PrimaryKeyRelatedField(many=True, read_only=True)
    groups = GroupSerializer(many=True, read_only=True)
    link = URLField(read_only=True, allow_null=True)

    class Meta:
        model = models.Event
        exclude = ("source",)


class EventSearchSerializer(HaystackSerializerMixin, EventSerializer):
    url = URLField(read_only=True, allow_null=True)

    class Meta(EventSerializer.Meta):
        field_aliases = None
        search_fields = ("text",)


class NewsMediaSerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `language`

    """

    media = MediaSerializer(read_only=True)
    expandable_fields = {"language": (LanguageSerializer, {"source": "language"})}

    class Meta:
        model = models.NewsMedia
        exclude = ("order", "news")


class NewsRelatedLinkSerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `language`

    """

    expandable_fields = {"language": (LanguageSerializer, {"source": "language"})}

    class Meta:
        model = models.NewsRelatedLink
        exclude = ("order", "news", "source")


class NewsRelatedMediaSerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `language`

    """

    media = MediaSerializer(read_only=True)
    expandable_fields = {"language": (LanguageSerializer, {"source": "language"})}

    class Meta:
        model = models.NewsRelatedMedia
        exclude = ("order", "news", "source")


class NewsSerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `categories`
     * `language`

    """

    expandable_fields = {
        "categories": (CategorySerializer, {"source": "categories", "many": True}),
        "language": (LanguageSerializer, {"source": "language"}),
    }
    url = URLField(read_only=True, allow_null=True)
    media = NewsMediaSerializer(many=True, read_only=True)
    breadcrumb = ReadOnlyField()
    categories = PrimaryKeyRelatedField(many=True, read_only=True)
    groups = GroupSerializer(many=True, read_only=True)
    related_links = NewsRelatedLinkSerializer(many=True, read_only=True)
    related_media = NewsRelatedMediaSerializer(many=True, read_only=True)

    class Meta:
        model = models.News
        exclude = ("source", "tags")


class NewsSearchSerializer(HaystackSerializerMixin, NewsSerializer):
    url = URLField(read_only=True, allow_null=True)

    class Meta(NewsSerializer.Meta):
        field_aliases = None
        search_fields = ("text",)


class ZMFCourseSerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `language`
     * `category`

    """

    expandable_fields = {
        "language": (LanguageSerializer, {"source": "language"}),
        "category": (CategorySerializer, {"source": "category"}),
    }

    class Meta:
        model = models.ZMFCourse
        exclude = ("page",)
