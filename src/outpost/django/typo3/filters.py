from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import (
    filters,
    filterset,
)

from . import models


class NewsFilter(filterset.FilterSet):
    '''
    ## Filters

    To filter for exact value matches:

        ?<fieldname>=<value>

    For advanced filtering use lookups:

        ?<fieldname>__<lookup>=<value>

    Possible lookups:

      - `datetime`: `gt`, `lt`, `gte`, `lte`, `date`
      - `title`: `iexact`, `contains`, `icontains`, `startswith`, `istartswith`, `endswith`, `iendswith`, `regex`, `iregex`
      - `teaser`: `iexact`, `contains`, `icontains`, `startswith`, `istartswith`, `endswith`, `iendswith`, `regex`, `iregex`
      - `start`: `gt`, `lt`, `gte`, `lte`, `date`
      - `end`: `gt`, `lt`, `gte`, `lte`, `date`
      - `author`: `iexact`, `contains`, `icontains`, `startswith`, `istartswith`, `endswith`, `iendswith`, `regex`, `iregex`
      - `email`: `iexact`, `contains`, `icontains`, `startswith`, `istartswith`, `endswith`, `iendswith`, `regex`, `iregex`
      - `keywords`: `iexact`, `contains`, `icontains`, `startswith`, `istartswith`, `endswith`, `iendswith`, `regex`, `iregex`
      - `last_modified`: `gt`, `lt`, `gte`, `lte`, `date`
    '''
    language = filters.ModelChoiceFilter(
        label=_('Language'),
        queryset=models.Language.objects.all()
    )
    categories = filters.ModelMultipleChoiceFilter(
        label=_('Categories'),
        queryset=models.Category.objects.all()
    )
    groups = filters.ModelMultipleChoiceFilter(
        label=_('Groups'),
        queryset=models.Group.objects.all()
    )

    class Meta:
        model = models.News
        fields = {
            'datetime': (
                'exact',
                'gt',
                'lt',
                'gte',
                'lte',
                'date',
            ),
            'title': (
                'exact',
                'iexact',
                'contains',
                'icontains',
                'startswith',
                'istartswith',
                'endswith',
                'iendswith',
                'regex',
                'iregex',
            ),
            'teaser': (
                'exact',
                'iexact',
                'contains',
                'icontains',
                'startswith',
                'istartswith',
                'endswith',
                'iendswith',
                'regex',
                'iregex',
            ),
            'start': (
                'exact',
                'gt',
                'lt',
                'gte',
                'lte',
                'date',
            ),
            'end': (
                'exact',
                'gt',
                'lt',
                'gte',
                'lte',
                'date',
            ),
            'author': (
                'exact',
                'iexact',
                'contains',
                'icontains',
                'startswith',
                'istartswith',
                'endswith',
                'iendswith',
                'regex',
                'iregex',
            ),
            'email': (
                'exact',
                'iexact',
                'contains',
                'icontains',
                'startswith',
                'istartswith',
                'endswith',
                'iendswith',
                'regex',
                'iregex',
            ),
            'keywords': (
                'exact',
                'iexact',
                'contains',
                'icontains',
                'startswith',
                'istartswith',
                'endswith',
                'iendswith',
                'regex',
                'iregex',
            ),
            'last_modified': (
                'exact',
                'gt',
                'lt',
                'gte',
                'lte',
                'date',
            ),
        }


class EventFilter(filterset.FilterSet):
    '''
    ## Filters

    To filter for exact value matches:

        ?<fieldname>=<value>

    For advanced filtering use lookups:

        ?<fieldname>__<lookup>=<value>

    Possible lookups:

      - `title`: `iexact`, `contains`, `icontains`, `startswith`, `istartswith`, `endswith`, `iendswith`, `regex`, `iregex`
      - `organizer`: `iexact`, `contains`, `icontains`, `startswith`, `istartswith`, `endswith`, `iendswith`, `regex`, `iregex`
      - `location`: `iexact`, `contains`, `icontains`, `startswith`, `istartswith`, `endswith`, `iendswith`, `regex`, `iregex`
      - `teaser`: `iexact`, `contains`, `icontains`, `startswith`, `istartswith`, `endswith`, `iendswith`, `regex`, `iregex`
      - `start`: `exact`, `gt`, `lt`, `gte`, `lte`, `contains`, `startswith`
      - `end`: `exact`, `gt`, `lt`, `gte`, `lte`, `contains`, `startswith`
      - `registration_end`: `exact`, `gt`, `lt`, `gte`, `lte`, `contains`, `startswith`
      - `dfp_points`: `exact`, `gt`, `lt`, `gte`, `lte`
      - `contact`: `iexact`, `contains`, `icontains`, `startswith`, `istartswith`, `endswith`, `iendswith`, `regex`, `iregex`
      - `email`: `iexact`, `contains`, `icontains`, `startswith`, `istartswith`, `endswith`, `iendswith`, `regex`, `iregex`
      - `last_modified`: `exact`, `gt`, `lt`, `gte`, `lte`, `contains`, `startswith`
    '''
    language = filters.ModelChoiceFilter(
        label=_('Language'),
        queryset=models.Language.objects.all()
    )
    calendar = filters.ModelChoiceFilter(
        label=_('Calendar'),
        queryset=models.Calendar.objects.all()
    )
    categories = filters.ModelMultipleChoiceFilter(
        label=_('Categories'),
        queryset=models.EventCategory.objects.all()
    )

    class Meta:
        model = models.Event
        fields = {
            'title': (
                'exact',
                'iexact',
                'contains',
                'icontains',
                'startswith',
                'istartswith',
                'endswith',
                'iendswith',
                'regex',
                'iregex',
            ),
            'organizer': (
                'exact',
                'iexact',
                'contains',
                'icontains',
                'startswith',
                'istartswith',
                'endswith',
                'iendswith',
                'regex',
                'iregex',
            ),
            'location': (
                'exact',
                'iexact',
                'contains',
                'icontains',
                'startswith',
                'istartswith',
                'endswith',
                'iendswith',
                'regex',
                'iregex',
            ),
            'teaser': (
                'exact',
                'iexact',
                'contains',
                'icontains',
                'startswith',
                'istartswith',
                'endswith',
                'iendswith',
                'regex',
                'iregex',
            ),
            'start': (
                'exact',
                'gt',
                'lt',
                'gte',
                'lte',
                'contains',
                'startswith',
            ),
            'end': (
                'exact',
                'gt',
                'lt',
                'gte',
                'lte',
                'contains',
                'startswith',
            ),
            'registration_end': (
                'exact',
                'gt',
                'lt',
                'gte',
                'lte',
                'contains',
                'startswith',
            ),
            'dfp_points': (
                'exact',
                'lt',
                'gt',
                'lte',
                'gte',
            ),
            'contact': (
                'exact',
                'iexact',
                'contains',
                'icontains',
                'startswith',
                'istartswith',
                'endswith',
                'iendswith',
                'regex',
                'iregex',
            ),
            'email': (
                'exact',
                'iexact',
                'contains',
                'icontains',
                'startswith',
                'istartswith',
                'endswith',
                'iendswith',
                'regex',
                'iregex',
            ),
            'last_modified': (
                'exact',
                'gt',
                'lt',
                'gte',
                'lte',
                'contains',
                'startswith',
            ),
        }
