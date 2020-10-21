from django import forms
from .models import author, audiobook


class author_form(forms.ModelForm):
    class Meta:
        model = author
        fields = ["title", "name_first", "name_mids", "name_last", "aliases", "birth", "death", "alive", "anzeige_name", "remarks"]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Titel", "aria-label": "title"}
            ),
            "name_first": forms.TextInput(
                attrs={"placeholder": "Vorname", "aria-label": "name_first"}
            ),
            "name_mids": forms.TextInput(
                attrs={"placeholder": "Zweitnamen", "aria-label": "name_mids"}
            ),
            "name_last": forms.TextInput(
                attrs={"placeholder": "Nachname", "aria-label": "name_last"}
            ),
            "aliases": forms.TextInput(
                attrs={"placeholder": "Aliase", "aria-label": "aliases"}
            ),
            "anzeige_name": forms.TextInput(
                attrs={"placeholder": "Anzeige Name", "aria-label": "anzeige_name"}
            ),
            "remarks": forms.Textarea(
                attrs={"placeholder": "Anmerkungen", "aria-label": "remarks", "rows": "5"}
            ),
        }

    def save(self, commit=True):
        model = super().save(commit=False)
        if not self.cleaned_data["anzeige_name"]:
            model.anzeige_name = ""
            if self.cleaned_data["name_first"]:
                model.anzeige_name = f"{str(self.cleaned_data['name_first'])} "
            model.anzeige_name += str(self.cleaned_data["name_last"])
        if commit:
            model.save()

        return model


class audiobook_form(forms.ModelForm):
    class Meta:
        model = audiobook
        fields = ["authors", "name", "release_book",
                  "release_book_germany", "release_as_audio", "synopsis",
                  "ro_ss", "shortened", "boxset", "boxset_name", "mp3CD",
                  "digital_only", "amount_CDs", "genre", "comments", "runtime"]