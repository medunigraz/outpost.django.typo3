from django.urls import path

from . import views

app_name = "typo3"

urlpatterns = [
    path("media/<int:pk>/", views.MediaView.as_view(), name="media"),
    path("media/<int:pk>/<int:width>", views.MediaView.as_view(), name="media"),
]
