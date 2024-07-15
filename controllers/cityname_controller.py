from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.CityName import CityName

router = APIRouter()

@router.get("/city_names")
async def index():
  try:
    cityname = CityName.get_city_names()
    return JSONResponse(status_code=200, content={"data": cityname})
  except Exception as e:
    return JSONResponse(status_code=500, content={"message": str(e)})

@router.get("/{city_name}")
async def show(city_name: str):
  try:
    towns = CityName.get_towns(city_name)
    if len(towns) == 0:
      return JSONResponse(status_code=404, content={"message": f"找不到 {city_name} 的鄉鎮資料"})
    return JSONResponse(status_code=200, content={"data": towns})
  except Exception as e:
    return JSONResponse(status_code=500, content={"message": str(e)})
