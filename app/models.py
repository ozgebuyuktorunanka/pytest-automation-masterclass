"""
Pydantic models.
type control and API validation process.
"""
from pydantic import BaseModel, EmailStr, field_validator


class User(BaseModel):
    id: int
    name: str
    email: str
    age: int

    # JS'deki custom validator gibi
    @field_validator("age")
    @classmethod
    def age_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("Age cannot be negative")
        if v > 150:
            raise ValueError("Age seems unrealistic")
        return v

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()


class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int = 0  # default value

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Price must be positive")
        return round(v, 2)


class CartItem(BaseModel):
    product_id: int
    quantity: int = 1

    @field_validator("quantity")
    @classmethod
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be at least 1")
        return v
