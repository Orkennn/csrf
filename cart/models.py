from typing import List

class CartItem:
    def __init__(self, product_id: int, quantity: int):
        self.product_id = product_id
        self.quantity = quantity

class Cart:
    def __init__(self):
        self.items: List[CartItem] = []

    def add_item(self, product_id: int, quantity: int):
        for item in self.items:
            if item.product_id == product_id:
                item.quantity += quantity
                return
        self.items.append(CartItem(product_id, quantity))

    def remove_item(self, product_id: int):
        self.items = [item for item in self.items if item.product_id != product_id]

    def clear(self):
        self.items.clear()

    def total_price(self, products):
        total = 0
        for item in self.items:
            product = next((p for p in products if p.id == item.product_id), None)
            if product:
                total += product.price * item.quantity
        return total
