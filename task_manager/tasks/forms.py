from django import forms
from django.utils.translation import gettext_lazy as _
from task_manager.tasks.models import Task
from django.contrib.auth import get_user_model


User = get_user_model()


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
        labels = {
            "name": _("Name"),
            "description": _("Description"),
            "status": _("Status"),
            "executor": _("Executor"),
            "labels": _("Labels"),
        }
        widgets = {
            "status": forms.Select(attrs={"class": "form-control"}),
            "executor": forms.Select(attrs={"class": "form-control"}),
            "labels": forms.SelectMultiple(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields["executor"].required = False
        self.fields["executor"].empty_label = "---------"
      
        self.fields["status"].required = False