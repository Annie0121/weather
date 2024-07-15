from fastapi import APIRouter
from fastapi.responses import JSONResponse
import requests

router = APIRouter()

CWB_API_KEY = "CWA-32805D52-091B-4553-93D4-F60AD3936AC8"

@router.get("/cityname")
async def index():
  try:
    cityname = ["臺北市", "新北市", "桃園市"]
    return {"data": cityname}
  except Exception as e:
    return JSONResponse(status_code=500, content={"message": str(e)})

@router.get("/weather/{cityname}")
async def get_weather(cityname: str):
  url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-093?Authorization={CWB_API_KEY}&locationName={cityname}"
  try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
  except requests.exceptions.RequestException as e:
    return JSONResponse(status_code=500, content={"message": str(e)})
  
  try:
    if "records" in data and "locations" in data["records"]:
      city_data = data['records']['locations'][0]
      districts_weather_data = []

      for district in city_data["location"]:
        district_name = district["locationName"]
        district_weather = []

        for element in district["weatherElement"]:
          if element["elementName"] == "T":
            for time_entry in element["time"]:
              forecast ={
                "startTime" : time_entry["startTime"],
                "endTime" : time_entry["endTime"],
                "temperature" : time_entry["elementValue"][0]["value"]
              }
              district_weather.append(forecast)

        districts_weather_data.append({
          "district": district_name,
          "forecast": district_weather
        })

      return{"city": cityname, "districts": districts_weather_data}
    else:
      return JSONResponse(status_code=500, content={"message": "資料錯誤"})
  except Exception as e:
    return JSONResponse(status_code=500, content={"message": str(e)})


  