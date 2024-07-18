from fastapi import APIRouter
from fastapi.responses import JSONResponse
import requests
import logging
from urllib.parse import quote
from models.CityName import CityName
import os
from dotenv import load_dotenv

router = APIRouter()

load_dotenv()
CWB_API_KEY = os.getenv('CWB_API_KEY')


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.get("/weather/{city_name}/{town_name}", responses={
    200: {
        "description": "The weather forecast for a specific city and town.",
        "content": {
            "application/json": {
                "example": {
                    "city": "臺北市",
                    "town": "信義區",
                    "weather": [
                        {
                            "date": "2024-07-18",
                            "time": "晚上",
                            "elementName": "MaxAT",
                            "description": "最高體感溫度",
                            "value": "34",
                        },
                        {
                            "date": "2024-07-18",
                            "time": "白天",
                            "elementName": "UVI",
                            "description": "紫外線指數",
                            "value": "11",
                        }
                    ]
                }
            }
        }
    },
    404: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "example": {
                    "message": "找不到指定的城市或鄉鎮的天氣資料"
                }
            }
        }
    },
    500: {
        "description": "Server error",
        "content": {
            "application/json": {
                "example": {
                    "message": "Internal server error"
                }
            }
        }
    }
})
async def get_weather(city_name: str, town_name: str):
    if town_name not in CityName.get_towns(city_name):
        return JSONResponse(status_code=404, content={"message": f"找不到 {city_name} 的鄉鎮 {town_name} 的天氣資料"})

    city_to_api_endpoint = {
        "宜蘭縣": "F-D0047-003",
        "桃園市": "F-D0047-007",  
        "新竹縣": "F-D0047-011",
        "苗栗縣": "F-D0047-015",
        "彰化縣": "F-D0047-019",
        "南投縣": "F-D0047-023",
        "雲林縣": "F-D0047-027",
        "嘉義縣": "F-D0047-031",
        "屏東縣": "F-D0047-035",
        "臺東縣": "F-D0047-039",
        "花蓮縣": "F-D0047-043",
        "澎湖縣": "F-D0047-047",
        "基隆市": "F-D0047-051",
        "新竹市": "F-D0047-055",
        "嘉義市": "F-D0047-059",
        "臺北市": "F-D0047-063",
        "高雄市": "F-D0047-067",  
        "新北市": "F-D0047-071",
        "臺中市": "F-D0047-075",
        "臺南市": "F-D0047-079",
        "連江縣": "F-D0047-083",
        "金門縣": "F-D0047-087",
    }

    # decoded_city_name = quote(city_name)
    if city_name not in city_to_api_endpoint:
        return JSONResponse(status_code=404, content={"message": f"找不到 {city_name} 的天氣API endpoint"})

    endpoint = city_to_api_endpoint[city_name]
    params = {
        "Authorization": CWB_API_KEY,
        "elementName": "MaxAT,UVI,PoP12h,RH",
        "locationName": town_name
    }
    
    url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/{endpoint}"

    headers = {
        "Accept": "application/json",
    }

    # logger.info(f"請求 {city_name} 的天氣數據")
    # logger.info(f"URL: {url}")

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        # logger.info(f"收到 {city_name} 的回應")
        # logger.debug(f"回應數據: {data}")

    except requests.exceptions.RequestException as e:
        # logger.error(f"獲取天氣數據時出錯: {e}")
        return JSONResponse(status_code=500, content={"message": str(e)})

    try:
        if "records" in data and "locations" in data["records"]:
            locations = data['records']['locations'][0]['location']
            
            town_data = next((loc for loc in locations if loc["locationName"] == town_name), None)
            
            if town_data is None:
                raise HTTPException(status_code=404, detail=f"未找到 {town_name} 的天氣數據")

            return process_weather_data(town_data, city_name, town_name)
        else:
            return JSONResponse(status_code=500, content={"message": "資料結構錯誤"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

def process_weather_data(town_data, city_name, town_name):
    weather_data = {}
    for element in town_data["weatherElement"]:
        if element["elementName"] in ["MaxAT", "UVI", "PoP12h", "RH"]:
            for time_entry in element["time"]:
                start_time = time_entry["startTime"]
                end_time = time_entry["endTime"]
                date = start_time.split(" ")[0]

                if (start_time[11:] == "06:00:00" and end_time[11:] == "18:00:00") or (start_time[11:] == "12:00:00" and end_time[11:] == "18:00:00"):
                    time_period = "白天"
                elif (start_time[11:] == "18:00:00" and end_time[11:] == "06:00:00") or (start_time[11:] == "00:00:00" and end_time[11:] == "06:00:00"):
                    time_period = "晚上"
                else:
                    continue

                key = (date, time_period)
                if key not in weather_data:
                    weather_data[key] = {}

                value = time_entry["elementValue"][0]["value"].strip()
                weather_data[key][element["elementName"]] = {
                    "description": element["description"],
                    "value": value if value else " "  # 如果值為空，使用空格(降雨機率)
                }

    # 將數據轉換格式並排序
    sorted_weather_data = []
    for (date, time_period), elements in sorted(weather_data.items()):
        for element_name in ["MaxAT", "UVI", "PoP12h", "RH"]:
            if element_name in elements:
                sorted_weather_data.append({
                    "date": date,
                    "time": time_period,
                    "elementName": element_name,
                    "description": elements[element_name]["description"],
                    "value": elements[element_name]["value"]
                })

    return {
        "city": city_name,
        "town": town_name,
        "weather": sorted_weather_data
    }
