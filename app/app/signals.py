from django.core.signals import got_request_exception
from django.dispatch import receiver
from .middleware import send_alert_discord

@receiver(got_request_exception)
def handle_exception(sender, request, **kwargs):
    discord_message = f"Exception détectée sur la vue - {request.path}"
    send_alert_discord(discord_message)
