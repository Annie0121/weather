from fastapi import APIRouter, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from controllers import cityname_controller, daily_weather_controller # 請後端同仁自行設定路由與 Controller 名稱

app = FastAPI()
router = APIRouter()

# 前端同仁自行調整資料存放位置
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
async def index(request: Request):
  return FileResponse("./static/index.html", media_type="text/html")


# 後端同仁自行設定路由與 Controller 名稱
app.include_router(cityname_controller.router, tags=["cityname"], prefix="/api/v1")
app.include_router(daily_weather_controller.router, tags=["weather","daily"], prefix="/api/v1")
