from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View

from task_manager.tasks.models import Task
from task_manager.users.forms import CreateUserForm
from task_manager.users.models import User


class BaseUserView(LoginRequiredMixin, View):
    login_url = "/login/"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, _("You are not logged in! Please sign in.")
            )
        return super().dispatch(request, *args, **kwargs)


class IndexUserView(View):
    def get(self, request):
        users = User.objects.all().order_by("id")
        return render(
            request,
            "users/index.html",
            context={"users": users},
        )


class CreateUserView(View):
    def get(self, request):
        return self._render_form(request, CreateUserForm())

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            messages.success(request, _("User registered successfully"))
            return redirect("login")
        return self._render_form(request, form)

    def _render_form(self, request, form):
        return render(request, "users/create.html", context={"form": form})


class UpdateUserView(BaseUserView):
    def get(self, request, pk):
        user = self._get_user(pk)
        if isinstance(user, HttpResponseRedirect):
            return user
        form = CreateUserForm(instance=user)
        return self._render_form(request, form, user)

    def post(self, request, pk):
        user = self._get_user(pk)
        if isinstance(user, HttpResponseRedirect):
            return user
        form = CreateUserForm(request.POST, instance=user)
        if form.is_valid():
            updated_user = form.save(commit=False)
            updated_user.set_password(form.cleaned_data["password1"])
            updated_user.save()
            messages.success(request, _("User successfully changed."))
            return redirect("users:index")
        return self._render_form(request, form, user)

    def _get_user(self, user_id):
        user = get_object_or_404(User, id=user_id)
        auth_user_id = self.request.user.id

        if auth_user_id != int(user_id) and not self.request.user.is_superuser:
            messages.error(
                self.request,
                _("You do not have permission to change another user."),
            )
            return redirect("users:index")
        return user

    def _render_form(self, request, form, user):
        return render(
            request, "users/update.html", context={"form": form, "user": user}
        )


class DeleteUserView(BaseUserView):
    def get(self, request, pk):
        user = self._get_user(pk)
        if isinstance(user, HttpResponseRedirect):
            return user
        return render(request, "users/delete.html", context={"user": user})

    def post(self, request, pk):
        user = self._get_user(pk)
        if isinstance(user, HttpResponseRedirect):
            return user
        if Task.objects.filter(executor=user).exists():
            messages.error(
                request, _("Cannot delete user because it is in use")
            )
            return redirect("users:index")
        user.delete()
        messages.success(request, _("User successfully deleted"))
        return redirect("users:index")

    def _get_user(self, user_id):
        user = get_object_or_404(User, id=user_id)
        auth_user_id = self.request.user.id

        if auth_user_id != int(user_id) and not self.request.user.is_superuser:
            messages.error(
                self.request,
                _("You do not have permission to change another user."),
            )
            return redirect("users:index")
        return user
