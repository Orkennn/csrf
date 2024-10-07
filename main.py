from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
import asyncio

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Добавляем middleware для работы с сессиями
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

# Укажите директорию для статических файлов и шаблонов
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Хранилище данных
data_store = {"count": 0}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "count": data_store["count"]})

@app.post("/change-data")
async def change_data(csrf_token: Optional[str] = Form(None)):
    if csrf_token != "token":
        raise HTTPException(status_code=403, detail="Invalid CSRF token")

    # Простой пример изменения данных
    data_store["count"] += 1
    return {"message": "Данные изменены", "new_count": data_store["count"]}

@app.post("/increment")
async def increment():
    # Имитация гонки, запускаем несколько асинхронных задач
    tasks = [increment_count() for _ in range(2)]
    await asyncio.gather(*tasks)
    return {"message": "Запущено изменение данных (Race Condition)"}

async def increment_count():
    await asyncio.sleep(1)  # Имитация задержки
    data_store["count"] += 1

print("test")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
