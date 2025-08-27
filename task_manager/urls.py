from django.contrib import admin
from django.urls import path, include

from task_manager.views import IndexView, LoginView, LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", IndexView.as_view(), name="index"),
    path("users/", include("task_manager.users.urls")), 
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]