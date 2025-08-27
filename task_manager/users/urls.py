from django.urls import path

from task_manager.users.views import (
    CreateUserView,
    DeleteUserView,
    IndexUserView,
    UpdateUserView,
)

app_name = "users"

urlpatterns = [
    path("", IndexUserView.as_view(), name="index"),
    path("create/", CreateUserView.as_view(), name="create"),
    path("<int:pk>/update/", UpdateUserView.as_view(), name="update"),
    path("<int:pk>/delete/", DeleteUserView.as_view(), name="delete"),
]