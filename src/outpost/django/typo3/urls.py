from django.conf.urls import url

from . import views

urlpatterns = [
        url(
            r'^media/(?P<pk>\d+)/(?P<width>\d+)?$',
            views.MediaView.as_view(),
            name='media'
        ),
]
