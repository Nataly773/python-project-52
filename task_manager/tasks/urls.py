from django.urls import path

from task_manager.tasks.views import (
    CreateTaskView,
    DeleteTaskView,
    IndexTaskView,
    ShowTaskView,
    UpdateTaskView,
)

app_name = "tasks"

urlpatterns = [
    path("", IndexTaskView.as_view(), name="index"),
    path("create/", CreateTaskView.as_view(), name="create"),
    path("<int:pk>/update/", UpdateTaskView.as_view(), name="update"),
    path("<int:pk>/delete/", DeleteTaskView.as_view(), name="delete"),
    path("<int:pk>/", ShowTaskView.as_view(), name="show"),
]