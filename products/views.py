from fastapi import APIRouter
from .models import Product  # Ваши модели товаров

router = APIRouter()

products = [
    {"id": 1, "name": "Товар 1", "price": 100, "quantity": 10},
    {"id": 2, "name": "Товар 2", "price": 200, "quantity": 5}
]

@router.get("/")
async def get_products():
    # Возвращаем список товаров
    return products
