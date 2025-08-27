from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label


class CreateLabelForm(forms.ModelForm):

    class Meta:
        model = Label
        fields = ["name"]
        labels = {"name": _("Name")}

    def clean_name(self):
        label_name = self.cleaned_data["name"]
        label = Label.objects.filter(name=label_name)

        if label.exists() and self.instance.pk != label[0].pk:
            raise forms.ValidationError(
                _("Task status with this Name already exists.")
            )
        return self.cleaned_data["name"]