from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import ListView
from task_manager.tasks.models import Task
from django.views.generic.edit import CreateView, UpdateView
from .forms import CreateStatusForm
from .models import Status


class BaseStatusView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")
    redirect_field_name = None

    def handle_no_permission(self):
        messages.error(
            self.request, 
            _("You are not logged in! Please sign in")
            )
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


class DeleteStatusesView(BaseStatusView):
    def get(self, request, pk):
        status = Status.objects.get(pk=pk)
        return render(
            request,
            "statuses/delete.html",
            context={
                "status": status,
            },
        )

    def post(self, request, pk):
        status = get_object_or_404(Status, pk=pk)
        if Task.objects.filter(status=status).exists():
            messages.error(
                request, _("Cannot delete status because it is in use")
            )
            return redirect("statuses:index")
        status.delete()
        messages.success(request, _("Status successfully deleted"))
        return redirect("statuses:index")