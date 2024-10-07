class Product:
    def __init__(self, id: int, name: str, description: str, price: float, quantity: int):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

# Пример данных товаров
products_data = [
    Product(id=1, name="Ноутбук", description="Игровой ноутбук", price=50000, quantity=10),
    Product(id=2, name="Смартфон", description="Смартфон с хорошей камерой", price=25000, quantity=20),
    Product(id=3, name="Часы", description="Умные часы", price=10000, quantity=15),
]
