import requests
import json
from datetime import datetime, timedelta
import time

def bot_sending(msg,pic):
    webhook_url = 'https://discord.com/api/webhooks/1162404320399085690/y6pNTIyURc4-ftZIicqF49uzwNTF70bRw_9D1QyVrmxzbwagnXXX-HNW2E6QvzUJVUVS'
    message = {
        'username': 'third',
        'content': msg,
        'embeds': [{'title': 'third',
                'image': {'url': pic}}]
    }
    response = requests.post(webhook_url, data=json.dumps(message), headers={'Content-Type': 'application/json'})
    print(response)
    if response.status_code == 204:
        print('204 -> Message sent successfully!')
    else:
        print(f'{response.status_code} -> {response.text}')

def get_next_turn():
    now = datetime.now()
    times = [
        now.replace(hour=6, minute=0, second=0, microsecond=0),
        now.replace(hour=12, minute=0, second=0, microsecond=0),
        now.replace(hour=18, minute=0, second=0, microsecond=0)
    ]
    turns = [t for t in times if t > now]
    if not turns:
        turns = [time + timedelta(days=1) for time in times]
    return turns[0]



while True:
    next = get_next_turn()
    sleep_till = (next - datetime.now()).total_seconds()
    time.sleep(sleep_till)
    m=''
    p=''
    bot_sending(m,p)


# m = "a test message from bot-3"
# p = 'https://memes.tw/user-gif-post/1721120277577.gif'
# p = 'https://memes.tw/user-gif-post/1721121188534.gif'