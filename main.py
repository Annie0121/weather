from fastapi import APIRouter, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from controllers import cityname_controller # 請後端同仁自行設定路由與 Controller 名稱
from controllers import week_weather_controller

app = FastAPI()
router = APIRouter()

# 前端同仁自行調整資料存放位置
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")

@app.get("/", include_in_schema=False)
async def index(request: Request):
  return FileResponse("./index.html", media_type="text/html")


# 後端同仁自行設定路由與 Controller 名稱
app.include_router(cityname_controller.router, tags=["cityname"], prefix="/api/v1")
app.include_router(week_weather_controller.router, tags=["week_weather"], prefix="/api/v1")