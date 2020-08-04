from django.conf.urls import url

from . import views

app_name = "typo3"

urlpatterns = [
    url(r"^media/(?P<pk>\d+)/(?P<width>\d+)?$", views.MediaView.as_view(), name="media")
]
