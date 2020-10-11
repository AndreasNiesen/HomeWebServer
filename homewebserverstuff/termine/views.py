from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView
from .forms import termin_form
from .models import termin as termin_model


def termineView(request):
    context = {}
    filterBy = request.GET.get("filterBy", None)
    filterValue = request.GET.get("filterValue", None)
    if filterBy and filterValue:
        filterBy = filterBy.lower()
        context["filterBy"] = filterBy
        context["filterValue"] = filterValue
        if filterBy == "user":
            context["termine"] = termin_model.objects.filter(user__username=f"{filterValue}")
        elif filterBy == "termin_name":
            context["termine"] = termin_model.objects.filter(termin_name=f"{filterValue}")
    else:
        context["termine"] = termin_model.objects.all()

    return render(request, "termine/termine.html", context)


def new_termin(request):
    if request.method == "POST":
        termine = termin_form(request.POST)
        if termine.is_valid():
            termine.save()
            messages.success(request, "Termin wurde registriert.")
            return redirect('termine_home')
        else:
            messages.error(request, "Ein Fehler ist aufgetreten.")
            print(request.POST)
    else:
        termine = termin_form()

    return render(request, "termine/neu.html", {"termine": termine})


class terminDetailView(DetailView):
    model = termin_model
    template_name = "termine/details.html"
    context_object_name = "termin"


class terminDeleteView(SuccessMessageMixin, DeleteView):
    model = termin_model
    template_name = "termine/delete.html"
    context_object_name = "termin"
    success_url = reverse_lazy("termine_home")
    success_message = "Termin erfolgreich gelöscht."

    # success_message alone doesn't work for DeleteViews
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(terminDeleteView, self).delete(request, *args, **kwargs)