from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/cityname")
async def index():
  try:
    cityname = ["臺北市", "新北市", "桃園市"]
    return {"data": cityname}
  except Exception as e:
    return JSONResponse(status_code=500, content={"message": str(e)})
