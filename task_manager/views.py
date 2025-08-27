from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.tasks.models import Task
from task_manager.users.forms import CreateUserForm
from task_manager.users.models import User


class UserPermissionMixin(UserPassesTestMixin):
    """Mixin: запрещает редактировать/удалять других пользователей."""

    def test_func(self):
        user = self.get_object()
        return self.request.user.is_superuser or self.request.user == user

    def handle_no_permission(self):
        messages.error(
            self.request,
            _("You do not have permission to change another user."),
        )
        return redirect("users:index")


class IndexUserView(ListView):
    model = User
    template_name = "users/index.html"
    context_object_name = "users"
    ordering = ["id"]


class CreateUserView(CreateView):
    model = User
    form_class = CreateUserForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password1"])
        user.save()
        messages.success(self.request, _("User registered successfully"))
        return super().form_valid(form)


class UpdateUserView(LoginRequiredMixin, UserPermissionMixin, UpdateView):
    model = User
    form_class = CreateUserForm
    template_name = "users/update.html"
    success_url = reverse_lazy("users:index")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password1"])
        user.save()
        messages.success(self.request, _("User successfully changed."))
        return super().form_valid(form)


class DeleteUserView(LoginRequiredMixin, UserPermissionMixin, DeleteView):
    model = User
    template_name = "users/delete.html"
    success_url = reverse_lazy("users:index")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        user = self.get_object()
        if Task.objects.filter(executor=user).exists():
            messages.error(
                self.request,
                _("Cannot delete user because it is in use"),
            )
            return redirect("users:index")
        messages.success(self.request, _("User successfully deleted"))
        return super().form_valid(form)
