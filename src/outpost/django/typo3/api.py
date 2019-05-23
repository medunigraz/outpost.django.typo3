from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_haystack.viewsets import HaystackViewSet
from rest_flex_fields.views import FlexFieldsMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from outpost.django.base.decorators import docstring_format

# from rest_framework_extensions.mixins import (
#     CacheResponseAndETAGMixin,
# )
# from rest_framework_extensions.cache.mixins import (
#     CacheResponseMixin,
# )
from . import (
    filters,
    models,
    serializers,
)


@docstring_format(model=models.Language.__doc__)
class LanguageViewSet(ReadOnlyModelViewSet):
    '''
    List languages from TYPO3.

    {model}
    '''
    queryset = models.Language.objects.all()
    serializer_class = serializers.LanguageSerializer
    permission_classes = (
        AllowAny,
    )
    filter_fields = (
        'isocode',
    )


@docstring_format(
    model=models.Category.__doc__,
    serializer=serializers.CategorySerializer.__doc__
)
class CategoryViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    '''
    List categories from TYPO3.

    {model}
    {serializer}
    '''
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (
        AllowAny,
    )
    filter_fields = (
        'language',
        'start',
        'end',
    )
    permit_list_expands = (
        'language',
    )


@docstring_format(
    model=models.Calendar.__doc__,
    serializer=serializers.CalendarSerializer.__doc__
)
class CalendarViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    '''
    List calendars from TYPO3.

    {model}
    {serializer}
    '''
    queryset = models.Calendar.objects.all()
    serializer_class = serializers.CalendarSerializer
    permission_classes = (
        AllowAny,
    )
    filter_fields = (
        'language',
    )
    permit_list_expands = (
        'language',
    )


@docstring_format(
    model=models.EventCategory.__doc__,
    serializer=serializers.EventCategorySerializer.__doc__
)
class EventCategoryViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    '''
    List event categories from TYPO3.

    {model}
    {serializer}
    '''
    queryset = models.EventCategory.objects.all()
    serializer_class = serializers.EventCategorySerializer
    permission_classes = (
        AllowAny,
    )
    filter_fields = (
        'calendar',
        'language',
    )
    permit_list_expands = (
        'calendar',
        'language',
    )


@docstring_format(
    model=models.Event.__doc__,
    filter=filters.EventFilter.__doc__,
    serializer=serializers.EventSerializer.__doc__
)
class EventViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    '''
    List events from TYPO3.

    {model}
    {filter}
    {serializer}
    '''
    queryset = models.Event.objects.filter(end__gte=timezone.now())
    serializer_class = serializers.EventSerializer
    permission_classes = (
        AllowAny,
    )
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_class = filters.EventFilter
    permit_list_expands = (
        'calendar',
        'language',
    )

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return self.queryset.exclude(source__private=True)
        return self.queryset


class EventSearchViewSet(HaystackViewSet):
    index_models = [models.Event]
    serializer_class = serializers.EventSearchSerializer
    permission_classes = (
        AllowAny,
    )


@docstring_format(
    model=models.News.__doc__,
    filter=filters.NewsFilter.__doc__,
    serializer=serializers.NewsSerializer.__doc__
)
class NewsViewSet(ReadOnlyModelViewSet):
    '''
    List news from TYPO3.

    {model}
    {filter}
    {serializer}
    '''
    queryset = models.News.objects.all()
    serializer_class = serializers.NewsSerializer
    permission_classes = (
        AllowAny,
    )
    filter_backends = (
        DjangoFilterBackend,
    )
    filter_class = filters.NewsFilter
    permit_list_expands = (
        'categories',
        'language',
    )

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return self.queryset.exclude(source__private=True)
        return self.queryset


class NewsSearchViewSet(HaystackViewSet):
    index_models = [models.News]
    serializer_class = serializers.NewsSearchSerializer
    permission_classes = (
        AllowAny,
    )
