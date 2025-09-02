from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import ListView
from task_manager.tasks.models import Task
from django.views.generic.edit import CreateView
from .forms import CreateStatusForm
from .models import Status
from django.views.generic.edit import DeleteView


class BaseStatusView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")
    redirect_field_name = None

    def handle_no_permission(self):
        messages.error(self.request, _("You are not logged in! Please sign in"))
        return super().handle_no_permission()


class IndexStatusesView(BaseStatusView, ListView):
    model = Status
    template_name = "statuses/index.html"
    context_object_name = "statuses"
    ordering = ["id"]


class CreateStatusesView(BaseStatusView, CreateView):
    model = Status
    form_class = CreateStatusForm
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("Status successfully created"))
        return response


from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import UpdateView
from task_manager.statuses.models import Status
from task_manager.statuses.forms import CreateStatusForm


class UpdateStatusesView(BaseStatusView, UpdateView):
    model = Status
    form_class = CreateStatusForm
    template_name = "statuses/update.html"
    success_url = reverse_lazy("statuses:index")
    context_object_name = "status"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("Status successfully updated"))
        return response

class DeleteStatusesView(BaseStatusView, DeleteView):
    model = Status
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses:index")
    context_object_name = "status"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if Task.objects.filter(status=self.object).exists():
            messages.error(
                request, _("Cannot delete status because it is in use")
            )
            return redirect("statuses:index")
        self.object.delete()
        messages.success(request, _("Status successfully deleted"))
        return redirect(self.success_url)