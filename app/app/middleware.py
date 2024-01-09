
# import time
# from app.models import RequestLog

# class RequestMiddleware:
#   def __init__(self, get_response):
#     self.get_response = get_response

#   def __call__(self, request):
#     start_time = time.time()
#     response = self.get_response(request)
#     duration = time.time() - start_time

#     RequestLog.objects.create(path=request.path, duration=duration)

#     return response

import requests

webhook_url = 'https://discord.com/api/webhooks/1194197927166496848/C5wdNbiKkmhTtWEzzMzaQiHZ6e2dGovuildVAMZWPYymtibCWqA-1EvRdC9m2nLPcvuZ'

def send_alert_discord(message):
    data = {
        "content": message,
        "username": "Bot de Monitoring"
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(webhook_url, json=data, headers=headers)
    print("Réponse Discord:", response.status_code, response.text)

import requests
from django.http import HttpResponseServerError

class DiscordErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            print("Exception capturée par le middleware :", str(e))  # Log pour débogage
            discord_message = f"ATTENTION : Exception non gérée sur la vue - {request.path} - {str(e)}"
            send_alert_discord(discord_message)
            return HttpResponseServerError("Une erreur interne est survenue.")
