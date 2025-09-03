from django.urls import path

from .views import (
    CreateStatusesView,
    DeleteStatusesView,
    IndexStatusesView,
    UpdateStatusesView,
   
)


app_name = "statuses"

urlpatterns = [
    path("", IndexStatusesView.as_view(), name="index"),
    path("create/", CreateStatusesView.as_view(), name="create"),
    path("<int:pk>/update/", UpdateStatusesView.as_view(), name="update"),
    path("<int:pk>/delete/", DeleteStatusesView.as_view(), name="delete"),
]