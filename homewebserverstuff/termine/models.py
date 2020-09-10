from django.db import models
from django.utils.timezone import localtime as lt
from django.contrib.auth.models import User


class termin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    termin_name = models.CharField(max_length=100)
    date = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    comment = models.TextField(blank=True)
    reminder = models.BooleanField(default=False)

    def __str__(self):
        return f"{lt(self.date).day:02d}.{lt(self.date).month:02d}.{lt(self.date).year:04d} "\
               f"{lt(self.date).hour:02d}:{lt(self.date).minute:02d} - "\
               f"{self.user.username} - "\
               f"{self.termin_name}"

    class Meta:
        ordering = ["-date", "user"]
        verbose_name_plural = "termine"