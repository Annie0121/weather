from fastapi import APIRouter
from fastapi.responses import JSONResponse
import requests
import logging
from urllib.parse import quote
from models.CityName import CityName

router = APIRouter()

CWB_API_KEY = "CWA-32805D52-091B-4553-93D4-F60AD3936AC8" #測試用 前端可先測試後再PR刪除即可

@router.get("/city_names")
async def get_city_names():
    try:
        city_names = CityName.get_city_names()
        return JSONResponse(status_code=200, content={"data": city_names})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@router.get("/{city_name}")
async def get_towns(city_name: str):
    try:
        towns = CityName.get_towns(city_name)
        if not towns:
            return JSONResponse(status_code=404, content={"message": f"找不到 {city_name} 的鄉鎮資料"})
        return JSONResponse(status_code=200, content={"data": towns})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/weather/{city_name}/{town_name}")
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
    url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/{endpoint}?Authorization={CWB_API_KEY}&elementName=T&locationName={quote(town_name)}"

    headers = {
        "Accept": "application/json",
    }

    logger.info(f"請求 {city_name} 的天氣數據")
    logger.info(f"URL: {url}")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        logger.info(f"收到 {city_name} 的回應")
        logger.debug(f"回應數據: {data}")

    except requests.exceptions.RequestException as e:
        logger.error(f"獲取天氣數據時出錯: {e}")
        return JSONResponse(status_code=500, content={"message": str(e)})

    try:
        if "records" in data and "locations" in data["records"]:
            locations = data['records']['locations'][0]['location']
            
            town_data = next((loc for loc in locations if loc["locationName"] == town_name), None)
            
            if town_name is None:
                raise HTTPException(status_code=404, detail=f"未找到 {town_name} 的天氣數據")

            weather_data = []

            for element in town_data["weatherElement"]:
                if element["elementName"] == "T":
                    for time_entry in element["time"]:
                        forecast = {
                            "startTime": time_entry["startTime"],
                            "endTime": time_entry["endTime"],
                            "temperature": time_entry["elementValue"][0]["value"]
                        }
                        weather_data.append(forecast)
          
            logger.info(f"回應處理成功，返回數據: {town_name}")
            return {"city": city_name,"town": town_name, "weather": weather_data}
        else:
            logger.error(f"資料結構錯誤")
            return JSONResponse(status_code=500, content={"message": "資料錯誤"})
    except Exception as e:
        logger.error(f"處理天氣數據時出錯: {e}")
        return JSONResponse(status_code=500, content={"message": str(e)})
