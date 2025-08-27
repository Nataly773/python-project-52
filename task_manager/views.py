from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View

from task_manager.forms import LoginForm


class IndexView(View):
    def get(self, request):
        return render(request, "index.html", context={})


class LoginView(View):
    def get(self, request):
        return self._render_form(request, LoginForm())

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, _("You are login"))
                return redirect("index")
            form.add_error(
                None,
                _(
                    "Please enter a correct username and password. "
                    "Note that both fields may be case-sensitive."
                ),
            )
        return self._render_form(request, form)

    def _render_form(self, request, form):
        return render(request, "login.html", context={"form": form})


class LogoutView(View):
    def get(self, request):
        return redirect("index")

    def post(self, request):
        logout(request)
        messages.info(request, _("You are logout"))
        return redirect("index")