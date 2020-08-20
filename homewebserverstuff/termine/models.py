from django.db import models
from django.contrib.auth.models import User


class termin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    termin_name = models.CharField(max_length=100)
    comment = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.date.date().day}.{self.date.date().month}.{self.date.date().year} {self.date.time().hour}:{self.date.time().minute} - {self.user.username}"

    class Meta:
        ordering = ["-date", "user"]
        verbose_name_plural = "termine"