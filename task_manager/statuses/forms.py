from django import forms
from django.utils.translation import gettext_lazy as _
from django.db import models

from task_manager.statuses.models import Status
    
class CreateStatusForm(forms.ModelForm):

    class Meta:
        model = Status
        fields = [
            "name",
        ]
        labels = {
            "name": _("Name"),
        }

    def clean_name(self):
        status_name = self.cleaned_data["name"]
        stasus = Status.objects.filter(name=status_name)

        if stasus.exists() and self.instance.pk != stasus[0].pk:
            raise forms.ValidationError(
                _("Task status with this Name already exists.")
            )
        return self.cleaned_data["name"]