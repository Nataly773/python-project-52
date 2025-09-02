from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Status


class CreateStatusForm(forms.ModelForm):

    class Meta:
        model = Status
        fields = ["name"]
        labels = {
            "name": _("Name"),
        }

    def clean_name(self):
        status_name = self.cleaned_data["name"]

        if (
            Status.objects.filter(name=status_name)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError(
                _("Task status with this name already exists")
            )

        return status_name