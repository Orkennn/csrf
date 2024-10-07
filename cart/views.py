from fastapi import APIRouter, Request, Form, HTTPException
from starlette.responses import HTMLResponse

from .models import Cart
from products.models import products_data

router = APIRouter()
cart = Cart()


@router.post("/add", response_class=HTMLResponse)
async def add_to_cart(request: Request, product_id: int = Form(...), quantity: int = Form(...)):
    # Ищем товар по ID
    product = next((p for p in products_data if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.quantity < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")

    # Добавляем товар в корзину
    cart.add_item(product_id, quantity)
    return {"message": "Товар добавлен в корзину"}


@router.get("/", response_class=HTMLResponse)
async def view_cart(request: Request):
    # Отображаем содержимое корзины
    total = cart.total_price(products_data)
    return {"items": cart.items, "total": total}


@router.post("/checkout", response_class=HTMLResponse)
async def checkout(request: Request):
    # Простая логика оформления заказа
    if not cart.items:
        return {"message": "Корзина пуста"}

    cart.clear()
    return {"message": "Заказ успешно оформлен"}
