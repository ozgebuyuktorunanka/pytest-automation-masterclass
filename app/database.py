"""
In-memory Database (mock db).
"""
from app.models import User, Product

# Basit bir dict-based in-memory store
# JavaScript'teki Map() gibi düşün
db: dict = {
    "users": {
        1: User(id=1, name="Alice Smith", email="alice@example.com", age=30),
        2: User(id=2, name="Bob Jones", email="bob@example.com", age=25),
    },
    "products": {
        1: Product(id=1, name="Laptop", price=999.99, stock=10),
        2: Product(id=2, name="Mouse", price=29.99, stock=50),
        3: Product(id=3, name="Keyboard", price=79.99, stock=25),
    },
    "cart": {},  # { user_id: [CartItem, ...] }
}


def reset_db():
    """
    Test'ler arası izolasyon için db'yi başlangıç durumuna döndürür.
    Bunu conftest.py'deki fixture'larda kullanacağız.
    """
    db["users"] = {
        1: User(id=1, name="Alice Smith", email="alice@example.com", age=30),
        2: User(id=2, name="Bob Jones", email="bob@example.com", age=25),
    }
    db["products"] = {
        1: Product(id=1, name="Laptop", price=999.99, stock=10),
        2: Product(id=2, name="Mouse", price=29.99, stock=50),
        3: Product(id=3, name="Keyboard", price=79.99, stock=25),
    }
    db["cart"] = {}
