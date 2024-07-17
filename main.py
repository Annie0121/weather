from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from controllers import cityname_controller, daily_weather_controller, weekly_weather_controller
from models.Bot import loop

app = FastAPI()
running = True

# 前端同仁自行調整資料存放位置
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
async def index(request: Request):
  return FileResponse("./static/index.html", media_type="text/html")


# 後端同仁自行設定路由與 Controller 名稱
app.include_router(cityname_controller.router, tags=["cityname"], prefix="/api/v1")
app.include_router(daily_weather_controller.router, tags=["daily_weather"], prefix="/api/v1")
app.include_router(weekly_weather_controller.router, tags=["weekly_weather"], prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    global running
    running = True
    loop()

@app.on_event("shutdown")  
async def shutdown_event():
  global running
  running = False