from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import DetailView
from .forms import termin_form
from .models import termin as termin_model


def termineView(request):
    context = {}
    filterBy = request.GET.get("filterBy", None)
    filterValue = request.GET.get("filterValue", None)
    if filterBy and filterValue:
        context["filterBy"] = filterBy
        context["filterValue"] = filterValue
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