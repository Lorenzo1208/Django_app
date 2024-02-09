
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
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseServerError

# URL du webhook Discord
webhook_url = 'https://discord.com/api/webhooks/1194197927166496848/C5wdNbiKkmhTtWEzzMzaQiHZ6e2dGovuildVAMZWPYymtibCWqA-1EvRdC9m2nLPcvuZ'

# Fonction pour envoyer des alertes sur Discord
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

# Middleware pour gérer les erreurs et notifier sur Discord
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

# Middleware pour bloquer les IP et envoyer des alertes
# class BlockIPMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         ip = request.META.get('REMOTE_ADDR')
#         if self.is_blocked(ip):
#             # Envoyer l'alerte sur Discord
#             send_alert_discord(f"L'adresse IP {ip} a été bloquée après plus de 100 requêtes en moins de 60 secondes.")
#             return HttpResponse("Blocked", status=403)

#         response = self.get_response(request)
#         return response

#     def is_blocked(self, ip):
#         request_count = cache.get(ip, 0)
#         if request_count > 1000:
#             return True
#         else:
#             cache.set(ip, request_count + 1, 60)  # Expire in 60 seconds
#             return False
