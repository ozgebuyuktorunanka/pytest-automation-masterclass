"""
Mock FastAPI app
"""
from fastapi import FastAPI, HTTPException
from app.models import User, Product, CartItem
from app.database import db

app = FastAPI(title="TestMasterclass Mock API", version="1.0.0")

# ── USERS ──────────────────────────────────────────

@app.get("/users", response_model=list[User])
def get_users():
    return list(db["users"].values())

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    user = db["users"].get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", response_model=User, status_code=201)
def create_user(user: User):
    if user.id in db["users"]:
        raise HTTPException(status_code=409, detail="User already exists")
    db["users"][user.id] = user
    return user

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    if user_id not in db["users"]:
        raise HTTPException(status_code=404, detail="User not found")
    del db["users"][user_id]

# ── PRODUCTS ───────────────────────────────────────

@app.get("/products", response_model=list[Product])
def get_products():
    return list(db["products"].values())

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = db["products"].get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products", response_model=Product, status_code=201)
def create_product(product: Product):
    db["products"][product.id] = product
    return product

# ── CART ───────────────────────────────────────────

@app.get("/cart/{user_id}", response_model=list[CartItem])
def get_cart(user_id: int):
    if user_id not in db["users"]:
        raise HTTPException(status_code=404, detail="User not found")
    return db["cart"].get(user_id, [])

@app.post("/cart/{user_id}", status_code=201)
def add_to_cart(user_id: int, item: CartItem):
    if user_id not in db["users"]:
        raise HTTPException(status_code=404, detail="User not found")
    if item.product_id not in db["products"]:
        raise HTTPException(status_code=404, detail="Product not found")
    cart = db["cart"].setdefault(user_id, [])
    for existing in cart:
        if existing.product_id == item.product_id:
            existing.quantity += item.quantity
            return {"message": "Quantity updated"}
    cart.append(item)
    return {"message": "Item added to cart"}
