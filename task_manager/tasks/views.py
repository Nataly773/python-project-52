from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import CreateTaskForm
from task_manager.tasks.models import Task


class BaseTaskView(LoginRequiredMixin, View):
    login_url = "/login/"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, _("You are not logged in! Please sign in.")
            )
        return super().dispatch(request, *args, **kwargs)


class IndexTaskView(BaseTaskView):
    def get(self, request):
        tasks = Task.objects.all()
        filterset = TaskFilter(request.GET, queryset=tasks, request=request)
        return render(
            request,
            "tasks/index.html",
            context={
                "form": filterset.form,
                "tasks": filterset.qs,
            },
        )


class CreateTaskView(BaseTaskView):
    def get(self, request):
        form = CreateTaskForm()
        return self._render_form(request, form)

    def post(self, request):
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            form.save_m2m()
            messages.success(request, _("Task successfully created"))
            # Заменяем redirect на явный HttpResponseRedirect
            return HttpResponseRedirect(reverse("tasks:index"))
        return self._render_form(request, form)

    def _render_form(self, request, form):
        return render(request, "tasks/create.html", context={"form": form})


class DeleteTaskView(BaseTaskView):
    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        if task.author.id != request.user.id:
            messages.error(
                request, _("A task can only be deleted by its author.")
            )
            return redirect("tasks:index")
        return render(
            request,
            "tasks/delete.html",
            context={
                "task": task,
            },
        )

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if task.author != request.user:
            messages.error(
                request, _("A task can only be deleted by its author.")
            )
            return redirect("tasks:index")
        task.delete()
        messages.success(request, _("Task successfully deleted"))
        return redirect("tasks:index")


class UpdateTaskView(BaseTaskView):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        return self._render_form(request, CreateTaskForm(instance=task), task)

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = CreateTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, _("Task successfully updated"))
            return redirect("tasks:index")
        return self._render_form(request, form, task)

    def _render_form(self, request, form, task):
        return render(
            request, "tasks/update.html", context={"form": form, "task": task}
        )


class ShowTaskView(BaseTaskView):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        return render(request, "tasks/show.html", context={"task": task})
