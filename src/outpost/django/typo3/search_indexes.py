from celery_haystack.indexes import CelerySearchIndex
from haystack import indexes, fields

from .models import Event, News


class NewsIndex(CelerySearchIndex, indexes.Indexable):
    text = fields.CharField(document=True, use_template=True)
    language = fields.FacetCharField(model_attr="language__title")
    datetime = fields.DateTimeField(model_attr="datetime", null=True)
    topnews = fields.FacetBooleanField(model_attr="topnews")

    def get_model(self):
        return News

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class EventIndex(CelerySearchIndex, indexes.Indexable):
    text = fields.CharField(document=True, use_template=True)
    language = fields.FacetCharField(model_attr="language__title")
    start = fields.DateTimeField(model_attr="start", null=True)
    end = fields.DateTimeField(model_attr="end", null=True)
    allday = fields.FacetBooleanField(model_attr="allday")
    register = fields.FacetBooleanField(model_attr="register")
    attending_fees = fields.FacetBooleanField(model_attr="attending_fees")

    def get_model(self):
        return Event

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
