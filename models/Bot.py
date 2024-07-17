import requests
import json
from datetime import datetime, timedelta
import time
import os
import asyncio

def fetch_info():
    try:
        headers = {"Authorization": os.getenv('CWB_API_KEY')}
        url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0003-001?Authorization=CWB-840CF1E7-FC59-4E06-81C9-F4BB79253855&StationId=466920&GeoInfo=CountyCode'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()['records']['Station'][0]
            dd = {
                'status':'success',
                'describe':data['WeatherElement']['Weather'],
                'temp':data['WeatherElement']['AirTemperature'],
                'humidity':data['WeatherElement']['RelativeHumidity'],
                'rain':data['WeatherElement']['Now']['Precipitation'],
                'SunshineDuration':data['WeatherElement']['SunshineDuration'],
                'UVIndex':data['WeatherElement']['UVIndex'],
                'DailyHigh':data['WeatherElement']['DailyExtreme']['DailyHigh']['TemperatureInfo']['AirTemperature'],
                'DailyLow':data['WeatherElement']['DailyExtreme']['DailyLow']['TemperatureInfo']['AirTemperature'],
                'visible':data['WeatherElement']['VisibilityDescription'],
            }
            return dd
        else:
            return {'status':'error','message':response.content.decode('utf-8')}
        
    except requests.exceptions.RequestException as e:
        return {"message": str(e)}
    except Exception as e:
        return {"message": str(e)}

def get_next_turn():
    now = datetime.now()
    times = [
        now.replace(hour=6, minute=0, second=0, microsecond=0),
        now.replace(hour=12, minute=0, second=0, microsecond=0),
        now.replace(hour=18, minute=0, second=0, microsecond=0),
        now.replace(hour=21, minute=0, second=0, microsecond=0)
    ]
    turns = [t for t in times if t > now]
    if not turns:
        turns = [time + timedelta(days=1) for time in times]
    return turns[0]

def bot_sending(msg): # pic
    webhook_url = 'https://discord.com/api/webhooks/1162404320399085690/y6pNTIyURc4-ftZIicqF49uzwNTF70bRw_9D1QyVrmxzbwagnXXX-HNW2E6QvzUJVUVS'
    message = {
        'username': 'third',
        'content': msg,
        # 'embeds': [{'title': '怎麼gif送不出去...',
        #         'image': {'url': 'https://memes.tw/user-wtf/1721231780404.jpg'}}]
    }
    response = requests.post(webhook_url, data=json.dumps(message), headers={'Content-Type': 'application/json'})
    if response.status_code == 204:
        print('204 -> Message sent successfully!')
    else:
        print(f'{response.status_code} -> {response.text}')

async def loop(running):
    while running():
        next = get_next_turn()
        sleep_till = (next - datetime.now()).total_seconds()
        await asyncio.sleep(sleep_till)
        if running:
            raw = fetch_info()
            if raw.get('status')=='success':
                m = f"""
**現在時間：**
{next}

**天氣描述：**
{raw['describe']}
**溫  度：**
{raw['temp']}
**濕  度：**
{raw['humidity']}
**雨  量：**
{raw['rain']}
**日照時長：**
{raw['SunshineDuration']}
**UV指數：**
{raw['UVIndex']}
**日最高溫：**
{raw['DailyHigh']}
**日最低溫：**
{raw['DailyLow']}
**能 見 度：**
{raw['visible']}
                    """        
            else:
                m = raw.get('message')
                # p=''
            bot_sending(m)