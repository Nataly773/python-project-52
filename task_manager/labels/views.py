from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View

from task_manager.labels.forms import CreateLabelForm
from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class BaseLabelsView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")
    redirect_field_name = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, _("You are not logged in! Please sign in.")
            )
        return super().dispatch(request, *args, **kwargs)


class IndexLabelsView(BaseLabelsView):
    def get(self, request):
        labels = Label.objects.all()
        return render(request, "labels/index.html", context={"labels": labels})


class CreateLabelsView(BaseLabelsView):
    def get(self, request):
        return self._render_form(request, CreateLabelForm())

    def post(self, request):
        form = CreateLabelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("The label was successfully created."))
            return redirect("labels:index")
        return self._render_form(request, form)

    def _render_form(self, request, form):
        return render(request, "labels/create.html", context={"form": form})


class UpdateLabelsView(BaseLabelsView):
    def get(self, request, pk):
        label = get_object_or_404(Label, pk=pk)
        return self._render_form(
            request, CreateLabelForm(instance=label), label
        )

    def post(self, request, pk):
        label = get_object_or_404(Label, pk=pk)
        form = CreateLabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.success(request, _("Label successfully updated"))
            return redirect("labels:index")
        return self._render_form(request, form, label)

    def _render_form(self, request, form, label):
        return render(
            request,
            "labels/update.html",
            context={
                "form": form,
                "label": label,
            },
        )


class DeleteLabelsView(BaseLabelsView):
    def get(self, request, pk):
        label = Label.objects.get(pk=pk)
        return render(
            request,
            "labels/delete.html",
            context={
                "label": label,
            },
        )

    def post(self, request, pk):
        label = get_object_or_404(Label, pk=pk)
        if Task.objects.filter(labels=label).exists():
            messages.error(
                request, _("Cannot delete label because it is in use")
            )
            return redirect("labels:index")
        label.delete()
        messages.success(request, _("Label successfully deleted"))
        return redirect("labels:index")
