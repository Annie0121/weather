# /v1/rest/datastore/F-D0047-089
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import os
import requests

current = datetime.now()
current_day = current.strftime("%Y-%m-%d")
next_day = (current + timedelta(days=1)).strftime("%Y-%m-%d")
url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-089"
params = {
    "sort": "time",
    "timeFrom": f'{current_day}T00:00:00',
    "timeTo": f"{next_day}T01:00:00",
}
headers = {"Authorization": os.getenv('CWB_API_KEY')}

router = APIRouter()
@router.get("/api/weather/daily", responses={
    200: {
        "description": "A JSONresponse containing all of today's weather information for the city.",
        "content": {
            "application/json": {
                "example": {
                    "data": [  
                        {'新竹縣': {'dailyTemperature': [
                            {
                            '2024-07-16 12:00:00': '35'
                            },
                            {
                            '2024-07-16 15:00:00': '35'
                            },
                            {
                            '2024-07-16 18:00:00': '32'
                            }
                        ],
                        'briefDescription': [
                            {
                            '2024-07-16 12:00:00': [
                                '晴'
                            ]
                            },
                            {
                            '2024-07-16 15:00:00': [
                                '晴'
                            ]
                            },
                            {
                            '2024-07-16 18:00:00': [
                                '晴'
                            ]
                            }
                        ],
                        'PoP6h': [
                            {
                            '2024-07-16 12:00:00': '20'
                            },
                            {
                            '2024-07-16 18:00:00': '20'
                            }
                        ],
                        'mixWeatherDescription': [
                            {
                            '2024-07-16 12:00:00': '晴。降雨機率 20%。溫度攝氏35度。悶熱。西北風 平均風速1-2級(每秒3公尺)。相對濕度65%。'
                            },
                            {
                            '2024-07-16 15:00:00': '晴。降雨機率 20%。溫度攝氏35度。悶熱。西北風 平均風速1-2級(每秒2公尺)。相對濕度66%。'
                            },
                            {
                            '2024-07-16 18:00:00': '晴。降雨機率 20%。溫度攝氏32度。悶熱。偏北風 平均風速<= 1級(每秒1公尺)。相對濕度71%。'
                            }
                        ]
                        }
                    },  {'金門縣': {'dailyTemperature':[],'briefDescription':[],'PoP6h':[],'mixWeatherDescription':[]}},
                        {'苗栗縣': {'dailyTemperature':[],'briefDescription':[],'PoP6h':[],'mixWeatherDescription':[]}},
                                        ]
                                    }
                                }
                            }
                        },
                        500: {
                            "description": "Server error.",
                            "content": {
                                "application/json": {
                                    "example": {
                                        "message": "Internal server error."
                                    }
                                }
                            }
                        }
})
async def get_daily_weather_info(request: Request):
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()['records']['locations'][0]['location']

            location_info = []
            for n in range(len(data)):
                raw = data[n]
                locationName = raw['locationName']
                we = raw['weatherElement']

                dt = we[3]['time']
                dailyTemperature = [{n['dataTime']:n['elementValue'][0]["value"]} for n in dt]
                bd = we[1]['time']
                briefDescription = [{n['startTime']:[n['elementValue'][0]['value']]} for n in bd]
                Ph = we[7]['time']
                PoP6h = [{n['startTime']:n['elementValue'][0]['value']} for n in Ph]
                md = we[6]['time']
                mixWeatherDescription = [{n['startTime']:n['elementValue'][0]['value']} for n in md]

                processed_data = {'dailyTemperature':dailyTemperature, 'briefDescription':briefDescription, 'PoP6h':PoP6h, 'mixWeatherDescription':mixWeatherDescription}
                location_info.append({locationName:processed_data})

            return JSONResponse(status_code=200, content=location_info)
        
        else:
            return JSONResponse(status_code=response.status_code, content=response.content.decode('utf-8'))

    except requests.exceptions.RequestException as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})