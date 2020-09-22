from django.contrib import admin
from .models import termin as termin_model
from .models import user_additionals

admin.site.register(termin_model)
admin.site.register(user_additionals)