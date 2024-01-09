# from django.http import JsonResponse
# from monitoring import send_alert_discord

# def custom_exception_handler(request, exception):
#     # Envoi d'une notification à Discord
#     discord_message = f"Erreur dans la vue : {request.path} - Exception : {str(exception)}"
#     send_alert_discord(discord_message)

#     # Réponse JSON d'erreur
#     return JsonResponse({"error": "Une erreur interne est survenue."}, status=500)
