import django_filters as df
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

User = get_user_model()


class TaskFilter(df.FilterSet):
    status = df.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_("Status"),
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="---------",
        required=False,
    )

    executor = df.ModelChoiceFilter(
        queryset=User.objects.all(),
        label=_("Executor"),
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="---------",
        required=False,
    )

    labels = df.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_("Label"),
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="---------",
        required=False,
    )

    self_tasks = df.BooleanFilter(
        label=_("Only my tasks"),
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        method="filter_self_tasks",
        required=False,
    )

    class Meta:
        model = Task
        fields = []

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.data:
            self.form.initial = {"status": "", "executor": "", "label": ""}
