# import requests

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
