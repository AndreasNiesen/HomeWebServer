from django import forms
from .models import termin
from django.utils import timezone
from django.contrib.admin.widgets import AdminSplitDateTime


class termin_form(forms.ModelForm):
    sdt = forms.SplitDateTimeField(widget=AdminSplitDateTime)
    endsdt = forms.SplitDateTimeField(widget=AdminSplitDateTime, required=False)

    class Meta:
        model = termin
        fields = ["user", "termin_name", "comment", "reminder"]
        widgets = {
            "termin_name": forms.TextInput(
                attrs={"class": "mb-2 mt-2", "placeholder": "Termin Name"}
            ),
            "comment": forms.Textarea(
                attrs={"class": "mb-2", "placeholder": "Termin Kommentar (optional)"}
            ),
        }

    def save(self, commit=True):
        model = super().save(commit=False)
        model.date = timezone.localtime(self.cleaned_data["sdt"])
        print(self.cleaned_data["endsdt"])
        print(timezone.localtime(self.cleaned_data["endsdt"]))
        if self.cleaned_data["endsdt"]:
            model.end = timezone.localtime(self.cleaned_data["endsdt"])
        if commit:
            model.save()

        return model