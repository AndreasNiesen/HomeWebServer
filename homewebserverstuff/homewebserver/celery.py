import os
from celery import Celery
from celery.schedules import crontab
import django
from django.utils import timezone
from django.db.models import Q
import discord
import asyncio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homewebserver.settings")
django.setup()
from django.conf import settings
from termine.models import termin as termin_model  # needs to follow django.setup(), so INSTALLED_APPS will be populated

app = Celery("homewebserver")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute="*/10"), termin_reminder.s(), name="termin_reminder")
    sender.add_periodic_task(crontab(hour=3, minute=1), termin_deleter.s(), name="termin_deleter")


@app.task
def termin_reminder():
    discord_client = discord.Client()
    filtered_termine = termin_model.objects.filter(date__gte=timezone.localtime()).filter(date__lte=timezone.localtime() + timezone.timedelta(days=1)).filter(reminder=True)
    termine_list = {}
    for filtered_termin in filtered_termine:
        termine_list[filtered_termin.user.user_additionals.discord_id] = filtered_termin

    @discord_client.event
    async def on_ready():
        for discord_id, termin_obj in termine_list.items():
            if discord_id:
                target_user = discord_client.get_user(int(discord_id))
                if target_user:
                    await target_user.send(f"Morgen steht um {timezone.localtime(termin_obj.date).hour:02d}:{timezone.localtime(termin_obj.date).minute:02d} ein Termin an:\n{termin_obj.termin_name}")
                else:
                    print(f"No User found for discord_id \"{discord_id}\"")
            termin_obj.reminder = False

        await discord_client.close()

    # async operation in sync program - hackish solution
    discord_loop = asyncio.get_event_loop()
    discord_loop.run_until_complete(discord_client.start(settings.DISCORD_CLIENT_ID))
    for termin_obj in termine_list.values():
        termin_obj.save()


@app.task
def termin_deleter():
    # roughly translates to sql: SELECT * FROM termin WHERE (date < timezone.localtime - 24 hours AND end is Null) OR (end < timezone.localtime - 24 hours)
    filtered_termine = termin_model.objects.filter(Q(Q(date__lt=timezone.localtime() - timezone.timedelta(days=1)) & Q(end=None)) | Q(end__lt=timezone.localtime() - timezone.timedelta(days=1)))
    for filtered_termin in filtered_termine:
        filtered_termin.delete()