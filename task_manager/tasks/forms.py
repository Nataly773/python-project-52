from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class SearchTaskForm(forms.ModelForm):
    self_tasks = forms.BooleanField(
        label=_("Only my tasks"),
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    label = forms.ModelChoiceField(
        queryset=Label.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
        label=_("Label"),
        empty_label="---------",
    )

    class Meta:
        model = Task
        fields = [
            "status",
            "executor",
            "label",
            "self_tasks",
        ]
        labels = {
            "status": _("Status"),
            "executor": _("Executor"),
        }
        widgets = {
            "status": forms.Select(attrs={"class": "form-control"}),
            "executor": forms.Select(attrs={"class": "form-control"}),
        }
        empty_label = {
            "status": "---------",
            "executor": "---------",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].required = False
        self.fields["executor"].required = False


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "status",
            "executor",
            "labels",
        ]
        labels = {
            "name": _("Name"),
            "description": _("Description"),
            "status": _("Status"),
            "executor": _("Executor"),
            "labels": _("Labels"),
        }
        widgets = {
            "status": forms.Select(attrs={"class": "form-control"}),
            "labels": forms.SelectMultiple(attrs={"class": "form-control"}),
        }
        empty_label = {
            "status": "---------",
            "executor": "---------",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["executor"].required = False