# import requests
# import json
# import mlflow
# import time
# import psutil

# # URL de votre endpoint de monitoring
# monitoring_url = 'http://127.0.0.1:8000/'

# # URL de webhook Discord
# webhook_url = 'https://discord.com/api/webhooks/1194197927166496848/C5wdNbiKkmhTtWEzzMzaQiHZ6e2dGovuildVAMZWPYymtibCWqA-1EvRdC9m2nLPcvuZ'

# def send_alert_discord(message):
#     data = {
#         "content": message,
#         "username": "Bot de Monitoring"
#     }
#     headers = {
#         "Content-Type": "application/json"
#     }
#     response = requests.post(webhook_url, json=data, headers=headers)
#     print("Réponse Discord:", response.status_code, response.text)

# # Configuration MLflow
# mlflow.set_tracking_uri(uri="http://127.0.0.1:8080")

# def monitor_website(url):
#     start_time = time.time()
    
#     try:
#         response = requests.get(url)
#         response_time = time.time() - start_time

#         # Enregistrement des métriques avec MLflow
#         with mlflow.start_run():
#             mlflow.log_metric("response_time", response_time)
#             mlflow.log_metric("error_rate", 1 if response.status_code != 200 else 0)
#             mlflow.log_metric("availability", 1)
#             bandwidth = len(response.content) / (response_time * 1024)  # en Ko/s
#             mlflow.log_metric("bandwidth", bandwidth)
#             cpu_utilization = psutil.cpu_percent()
#             mlflow.log_metric("cpu_utilization", cpu_utilization)

#         # Préparation et envoi du message à Discord
#         discord_message = f"Monitoring : Temps de réponse = {response_time} secondes, Bande passante = {bandwidth} Ko/s, CPU = {cpu_utilization}%"
#         send_alert_discord(discord_message)

#     except Exception as e:
#         print(f"Erreur lors de la récupération des données de monitoring : {e}")
#         send_alert_discord(f"Erreur de monitoring : {e}")

# # Boucle de monitoring
# while True:
#     monitor_website(monitoring_url)
#     time.sleep(30)  # Pause de 5 secondes avant la prochaine itération

import requests
import time

# URL de votre endpoint de monitoring
monitoring_url = 'http://127.0.0.1:8000/'

# URL de webhook Discord
webhook_url = 'https://discord.com/api/webhooks/1194197927166496848/C5wdNbiKkmhTtWEzzMzaQiHZ6e2dGovuildVAMZWPYymtibCWqA-1EvRdC9m2nLPcvuZ'

def send_alert_discord(message_json):
    data = {
        "username": "Bot de Monitoring",
        "embeds": [
            message_json
        ]
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(webhook_url, json=data, headers=headers)
    print("Réponse Discord:", response.status_code, response.text)

def monitor_website(url):
    start_time = time.time()
    
    try:
        response = requests.get(url)
        response_time = time.time() - start_time
        bandwidth = len(response.content) / (response_time * 1024)  # en Ko/s

        # Préparation et envoi du message à Discord
        discord_message = f"Monitoring : Temps de réponse = {response_time:.2f} secondes, Bande passante = {bandwidth:.2f} Ko/s"
        
        discord_json = {
            "title": "Monitoring",
            "description": discord_message,
            "fields": [
                {
                    "name": "Temps de réponse",
                    "value": f"{response_time:.2f} secondes",
                    "inline": True
                },
                {
                    "name": "Bande passante",
                    "value": f"{bandwidth:.2f} Ko/s",
                    "inline": True
                },
            ]
        }
        send_alert_discord(discord_json)

    except Exception as e:
        print(f"Erreur lors de la récupération des données de monitoring : {e}")
        send_alert_discord(f"Erreur de monitoring : {e}")

# Boucle de monitoring
while True:
    monitor_website(monitoring_url)
    time.sleep(30)  # Pause de 30 secondes avant la prochaine itération
