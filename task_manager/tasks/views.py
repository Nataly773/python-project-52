from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreateTaskForm
from .models import Task
from django.shortcuts import get_object_or_404
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import CreateTaskForm


# Базовый класс для всех представлений задач
class BaseTaskView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")
    template_name = None  # будем задавать в наследниках

# Создание задачи

class CreateTaskView(BaseTaskView):
    template_name = "tasks/create.html"
    form_class = CreateTaskForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            form.save_m2m()
            messages.success(request, _("Task successfully created"))
            return HttpResponseRedirect(reverse("tasks:index"))
        return render(request, self.template_name, {"form": form})

# Список задач

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




class DeleteTaskView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        """Проверка, что пользователь — автор задачи, до любого метода."""
        self.task = get_object_or_404(Task, pk=kwargs["pk"])
        if self.task.author != request.user:
            messages.error(request, _("A task can only be deleted by its author."))
            return redirect("tasks:index")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(
            request,
            "tasks/delete.html",
            context={"task": self.task},
        )

    def post(self, request, *args, **kwargs):
        self.task.delete()
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