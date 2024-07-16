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
@router.get("/api/weather/daily")
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