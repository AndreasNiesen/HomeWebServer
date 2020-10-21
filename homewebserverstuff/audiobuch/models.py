from django.db import models
from django.urls import reverse


# author.audiobook_set <-> audiobook.authors
# audiobook.va_set <-> va.audiobooks
# role.vas <-> va.role_set
# role.audiobooks <-> audiobook.role_set
# audiobook.altName_set <-> altName.audiobook


class author(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    name_first = models.CharField(max_length=100, blank=True, null=True)
    name_mids = models.CharField(max_length=300, blank=True, null=True)
    name_last = models.CharField(max_length=100)
    aliases = models.CharField(max_length=500, blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    death = models.DateField(blank=True, null=True)
    alive = models.BooleanField(default=False)
    anzeige_name = models.CharField(max_length=300, blank=True, null=True)
    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ["anzeige_name", "birth"]

    def __str__(self):
        if self.anzeige_name:
            return self.anzeige_name
        else:
            full_name = (((self.title + " ") if self.title else "")
                        + ((self.name_first + " ") if self.name_first else "")
                        + ((self.name_mids + " ") if self.name_mids else "")
                        + self.name_last)
            return full_name

    def get_absolute_url(self):
        return reverse("author_details", kwargs={"pk": self.pk})


class audiobook(models.Model):
    authors = models.ManyToManyField(author)
    name = models.CharField(max_length=300)
    release_book = models.DateField(blank=True, null=True)
    release_book_germany = models.DateField(blank=True, null=True)
    release_as_audio = models.DateField(blank=True, null=True)
    synopsis = models.TextField(blank=True, null=True)
    ro_ss_choices = [
        ("ss", "Kurzgeschichte"),  # ss = short story
        ("ro", "Roman"),
    ]
    ro_ss = models.CharField(max_length=len(ro_ss_choices), choices=ro_ss_choices, default="ro", blank=False)
    shortened = models.BooleanField(default=False)
    boxset = models.BooleanField(default=False)
    boxset_name = models.CharField(max_length=100, blank=True, null=True)
    mp3CD = models.BooleanField(default=False)
    digital_only = models.BooleanField(default=False)
    amount_CDs = models.PositiveIntegerField()
    genre = models.CharField(max_length=150)
    comments = models.TextField(blank=True, null=True)
    runtime = models.TimeField()


class va(models.Model):  # Voice Actor
    audiobooks = models.ManyToManyField(audiobook)
    title = models.CharField(max_length=100, blank=True, null=True)
    name_first = models.CharField(max_length=100, blank=True, null=True)
    name_mids = models.CharField(max_length=300, blank=True, null=True)
    name_last = models.CharField(max_length=100)

    class Meta:
        ordering = ["name_last", "name_first"]
        verbose_name = "voice actor"
        verbose_name_plural = "voice actors"

    def __str__(self):
        full_name = (((self.title + " ") if self.title else "")
                    + ((self.name_first + " ") if self.name_first else "")
                    + ((self.name_mids + " ") if self.name_mids else "")
                    + self.name_last)
        return full_name


class role(models.Model):
    audiobooks = models.ManyToManyField(audiobook)
    vas = models.ManyToManyField(va)  # Voice ActorS
    title = models.CharField(max_length=100, blank=True, null=True)
    name_first = models.CharField(max_length=100, blank=True, null=True)
    name_mids = models.CharField(max_length=300, blank=True, null=True)
    name_last = models.CharField(max_length=100)

    class Meta:
        ordering = ["name_last", "name_first"]

    def __str__(self):
        full_name = (((self.title + " ") if self.title else "")
                    + ((self.name_first + " ") if self.name_first else "")
                    + ((self.name_mids + " ") if self.name_mids else "")
                    + self.name_last)
        return full_name


class altName(models.Model):
    audiobook = models.ForeignKey(audiobook, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    comment = models.TextField(blank=True, null=True)