from fastapi import FastAPI, Form, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, List
from hashlib import sha256
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

# Хранилище пользователей и товаров
users_db = {}
products_db = []
cart_db = {}


class User(BaseModel):
    username: str
    password: str


class Product(BaseModel):
    id: int
    name: str
    price: float
    quantity: int


class CartItem(BaseModel):
    product_id: int
    quantity: int


# Функция хеширования пароля
def hash_password(password: str) -> str:
    return sha256(password.encode()).hexdigest()


# Маршрут для главной страницы
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "count": data_store["count"]})


# Регистрация пользователя
@app.post("/register")
async def register(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    users_db[user.username] = hash_password(user.password)
    return {"message": "Регистрация прошла успешно"}


# Вход пользователя
@app.post("/login")
async def login(user: User, request: Request):
    stored_password = users_db.get(user.username)
    if stored_password is None or stored_password != hash_password(user.password):
        raise HTTPException(status_code=400, detail="Неверные данные для входа")

    request.session["user"] = user.username
    return {"message": f"Добро пожаловать, {user.username}"}


# Выход пользователя
@app.post("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return {"message": "Вы вышли из системы"}


# Профиль пользователя
@app.get("/profile")
async def profile(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=403, detail="Необходима авторизация")
    return {"message": f"Профиль пользователя: {user}"}


# Добавить товар
@app.post("/products/")
async def add_product(product: Product):
    products_db.append(product)
    return product


# Получить список товаров
@app.get("/products/", response_class=HTMLResponse)
async def list_products(request: Request):
    return templates.TemplateResponse("products.html", {"request": request, "products": products_db})


# Добавить товар в корзину
@app.post("/cart/add")
async def add_to_cart(cart_item: CartItem, request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=403, detail="Необходима авторизация")

    cart = cart_db.get(user, [])
    cart.append(cart_item)
    cart_db[user] = cart
    return {"message": "Товар добавлен в корзину"}


# Оформить заказ
@app.post("/cart/checkout")
async def checkout(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=403, detail="Необходима авторизация")

    cart = cart_db.get(user, [])
    total_price = 0
    for item in cart:
        product = next((p for p in products_db if p.id == item.product_id), None)
        if product is None or product.quantity < item.quantity:
            raise HTTPException(status_code=400, detail="Недостаточно товаров")
        product.quantity -= item.quantity
        total_price += product.price * item.quantity

    cart_db[user] = []  # Очищаем корзину после покупки
    return {"message": "Покупка завершена", "total": total_price}


# Изменить данные (имитация CSRF-защиты)
@app.post("/change-data")
async def change_data(csrf_token: Optional[str] = Form(None)):
    if csrf_token != "token":
        raise HTTPException(status_code=403, detail="Invalid CSRF token")

    data_store["count"] += 1
    return {"message": "Данные изменены", "new_count": data_store["count"]}


# Гонка за ресурсами (Race Condition)
@app.post("/increment")
async def increment():
    tasks = [increment_count() for _ in range(2)]
    await asyncio.gather(*tasks)
    return {"message": "Запущено изменение данных (Race Condition)"}


async def increment_count():
    await asyncio.sleep(1)  # Имитация задержки
    data_store["count"] += 1


# Старт сервера
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
