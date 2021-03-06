from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import author_form, audiobook_form
from .models import audiobook as audiobook_model
from .models import author as author_model


def authors_home(request):
    context = {}
    context["request"] = request
    pagination_page = request.GET.get("page", 1)
    filterBy = request.GET.get("filterBy", None)
    filterValue = request.GET.get("filterValue", None)
    if filterBy and filterValue:
        filterBy = filterBy.lower()
        context["filterBy"] = filterBy
        context["filterValue"] = filterValue
        if filterBy == "title":
            authors = author_model.objects.filter(title=f"{filterValue}")
        elif filterBy == "vorname":
            authors = author_model.objects.filter(name_first=f"{filterValue}")
        elif filterBy == "zweitname":
            authors = author_model.objects.filter(name_mids__contains=f"{filterValue}")
        elif filterBy == "nachname":
            authors = author_model.objects.filter(name_last=f"{filterValue}")
        elif filterBy == "alias":
            authors = author_model.objects.filter(aliases__contains=f"{filterValue}")
        elif filterBy == "anzeigename":
            authors = author_model.objects.filter(anzeige_name__contains=f"{filterValue}")
    else:
        authors = author_model.objects.all()

    paginator = Paginator(authors, 10)
    try:
        context["authors"] = paginator.page(pagination_page)
    except PageNotAnInteger:
        messages.warning(request, "Das page-attribut akzeptiert nur Ints!")
        context["authors"] = paginator.page(1)
    except EmptyPage:
        messages.info(request, "Diese Seitenzahl existiert nicht.")
        context["authors"] = paginator.page(paginator.num_pages)

    return render(request, "audiobuch/authors.html", context)


def new_author(request):
    if request.method == "POST":
        author = author_form(request.POST)
        if author.is_valid():
            author.save()
            messages.success(request, "Autor erstellt.")
            return redirect('authors_home')
        else:
            messages.error(request, "Ein Fehler ist aufgetreten.")
            print(request.POST)
    else:
        author = author_form()

    return render(request, "audiobuch/new_author.html", {"author": author})


class authorDetailView(DetailView):
    model = author_model
    template_name = "audiobuch/details_author.html"
    context_object_name = "author"


class authorUpdateView(UpdateView):
    model = author_model
    template_name = "audiobuch/edit_author.html"
    context_object_name = "author"
    fields = ["title", "name_first", "name_mids", "name_last", "aliases", "birth", "death", "alive", "anzeige_name", "remarks"]

    def form_valid(self, form):
        if not form.instance.anzeige_name:
            anzeige_name = ""
            if form.instance.name_first:
                anzeige_name = f"{ str(form.instance.name_first) } "
            anzeige_name += str(form.instance.name_last)
            form.instance.anzeige_name = anzeige_name
        return super().form_valid(form)


class authorDeleteView(SuccessMessageMixin, DeleteView):
    model = author_model
    template_name = "audiobuch/delete_author.html"
    context_object_name = "author"
    success_url = reverse_lazy("authors_home")
    success_message = "Autor erfolgreich gelöscht."

    # success_message alone doesn't work for DeleteViews
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(authorDeleteView, self).delete(request, *args, **kwargs)


def audiobView(request):
    context = {}
    context["audiobooks"] = audiobook_model.objects.all()

    return render(request, "audiobuch/audiob.html", context)


class audiobDetailView(DetailView):
    model = audiobook_model
    template_name = "audiobuch/details_audiob.html"
    context_object_name = "audiobook"


def new_audiobook(request):
    if request.method == "POST":
        audiobook = audiobook_form(request.POST)
        if audiobook.is_valid():
            audiobook.save()
            messages.success(request, "Audiobuch-Eintrag erstellt.")
            return redirect('audiob_home')
        else:
            messages.error(request, "Ein Fehler ist aufgetreten")
            print(request.POST)
    else:
        audiobook = audiobook_form()

    return render(request, "audiobuch/new_audiob.html", {"audiobook": audiobook})