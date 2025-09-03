from django.urls import path

from .views import (
    CreateLabelsView,
    DeleteLabelsView,
    IndexLabelsView,
    UpdateLabelsView,
)

app_name = 'labels'

urlpatterns = [
    path("", IndexLabelsView.as_view(), name="index"),
    path("create/", CreateLabelsView.as_view(), name="create"),
    path("<int:pk>/update/", UpdateLabelsView.as_view(), name="update"),
    path("<int:pk>/delete/", DeleteLabelsView.as_view(), name="delete"),
]