from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from cart.views import router as cart_router
from products.models import products_data
from auth.schemas import UserLoginSchema

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

# Роутинг для корзины
app.include_router(cart_router, prefix="/cart", tags=["cart"])

# Хранилище данных для имитации
data_store = {"count": 0}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "count": data_store["count"], "products": products_data})

@app.post("/change-data")
async def change_data(csrf_token: str = Form(...)):
    if csrf_token != "token":
        raise HTTPException(status_code=403, detail="Invalid CSRF token")

    # Простой пример изменения данных
    data_store["count"] += 1
    return {"message": "Данные изменены", "new_count": data_store["count"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
