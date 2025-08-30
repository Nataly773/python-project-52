from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View

from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import CreateTaskForm
from task_manager.tasks.models import Task

from django.core.paginator import Paginator



class BaseTaskView(LoginRequiredMixin, View):
    login_url = "/login/"


class IndexTaskView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request):
        # Оптимизированный queryset
        tasks = Task.objects.select_related('author', 'executor').prefetch_related('labels')

        # Применяем фильтр
        filterset = TaskFilter(request.GET, queryset=tasks, request=request)
        filtered_tasks = filterset.qs

        # Пагинация: 20 задач на страницу
        paginator = Paginator(filtered_tasks, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Передаем page_obj в шаблон
        return render(request, "tasks/index.html", context={
            "form": filterset.form,
            "tasks": page_obj,
        })

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

            # Сохранение ManyToMany меток быстрее через .set()
            if 'labels' in form.cleaned_data:
                task.labels.set(form.cleaned_data['labels'])

            # Сообщение об успешном создании задачи
            messages.success(request, _("Задача успешно создана"))

            # Редирект на индекс задач
            return redirect("tasks:index")
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