from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models.CityName import CityName

router = APIRouter()

@router.get("/city_names", responses={
    200: {
        "description": "A list of city names.",
        "content": {
            "application/json": {
                "example": {
                    "data": [
                        "臺北市", "新北市", "基隆市", "桃園市", "新竹縣", "新竹市", "苗栗縣",
                        "臺中市", "南投縣", "彰化縣", "雲林縣", "嘉義縣", "嘉義市", "臺南市",
                        "高雄市", "屏東縣", "宜蘭縣", "花蓮縣", "臺東縣", "澎湖縣", "金門縣", "連江縣"
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
async def get_city_names():
    try:
        city_names = CityName.get_city_names()
        return JSONResponse(status_code=200, content={"data": city_names})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@router.get("/{city_name}", responses={
    200: {
        "description": "Towns of the specified city.",
        "content": {
            "application/json": {
                "example": {
                    "data": [
                        "桃園區", "中壢區", "平鎮區", "八德區", "楊梅區", "蘆竹區", "龜山區",
                        "龍潭區", "大溪區", "大園區", "觀音區", "新屋區", "復興區"
                    ]
                }
            }
        }
    },
    404: {
        "description": "City not found.",
        "content": {
            "application/json": {
                "example": {
                    "message": "找不到 {city_name} 的鄉鎮資料"
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
async def get_towns(city_name: str):
    try:
        towns = CityName.get_towns(city_name)
        if not towns:
            raise HTTPException(status_code=404, detail=f"找不到 {city_name} 的鄉鎮資料")
        return JSONResponse(status_code=200, content={"data": towns})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
