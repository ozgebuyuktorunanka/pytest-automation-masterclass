"""
Unit Testler — app/models.py için

Bu testler:
- Dış bağımlılık yok (DB, network, browser)
- En hızlı çalışan testler
- @pytest.mark.unit ile işaretli

JS'deki Jest unit testleriyle birebir karşılaştırma:

  Jest:                              pytest:
  ─────────────────────────────────────────────────────
  describe('User model', () => {  →  class TestUserModel:
    it('creates valid user', () => {  →  def test_creates_valid_user(self):
      expect(user.name).toBe('Alice') →  assert user.name == "Alice"
    })
  })
"""
import pytest
from pydantic import ValidationError

from app.models import User, Product, CartItem


# ──────────────────────────────────────────────────────
# Class ile gruplamak opsiyonel ama organizasyon sağlar
# JS'deki describe() bloğu gibi
# ──────────────────────────────────────────────────────

class TestUserModel:

    @pytest.mark.unit
    def test_creates_valid_user(self):
        """Happy path: geçerli user oluşturulabilmeli."""
        user = User(id=1, name="Alice", email="alice@test.com", age=30)

        assert user.id == 1
        assert user.name == "Alice"
        assert user.email == "alice@test.com"
        assert user.age == 30

    @pytest.mark.unit
    def test_negative_age_raises_error(self):
        """Negatif yaş ValidationError fırlatmalı."""
        # JS'deki: expect(() => new User({age: -1})).toThrow()
        with pytest.raises(ValidationError) as exc_info:
            User(id=1, name="Alice", email="alice@test.com", age=-5)

        # Hata mesajını da kontrol edebiliriz
        assert "Age cannot be negative" in str(exc_info.value)

    @pytest.mark.unit
    def test_unrealistic_age_raises_error(self):
        with pytest.raises(ValidationError):
            User(id=1, name="Alice", email="alice@test.com", age=200)

    @pytest.mark.unit
    def test_empty_name_raises_error(self):
        with pytest.raises(ValidationError) as exc_info:
            User(id=1, name="   ", email="alice@test.com", age=30)
        assert "Name cannot be empty" in str(exc_info.value)

    @pytest.mark.unit
    def test_name_is_stripped(self):
        """Baştaki/sondaki boşluklar temizlenmeli."""
        user = User(id=1, name="  Alice  ", email="alice@test.com", age=30)
        assert user.name == "Alice"  # strip() uygulandı


class TestProductModel:

    @pytest.mark.unit
    def test_creates_valid_product(self):
        product = Product(id=1, name="Laptop", price=999.99, stock=10)
        assert product.price == 999.99
        assert product.stock == 10

    @pytest.mark.unit
    def test_default_stock_is_zero(self):
        """stock belirtilmezse 0 olmalı."""
        product = Product(id=1, name="Laptop", price=999.99)
        assert product.stock == 0

    @pytest.mark.unit
    def test_negative_price_raises_error(self):
        with pytest.raises(ValidationError):
            Product(id=1, name="Laptop", price=-10.0)

    @pytest.mark.unit
    def test_zero_price_raises_error(self):
        with pytest.raises(ValidationError):
            Product(id=1, name="Laptop", price=0)

    @pytest.mark.unit
    def test_price_is_rounded_to_two_decimals(self):
        """Fiyat 2 decimal'a yuvarlanmalı."""
        product = Product(id=1, name="Laptop", price=99.999)
        assert product.price == 100.0


class TestCartItemModel:

    @pytest.mark.unit
    def test_default_quantity_is_one(self):
        item = CartItem(product_id=1)
        assert item.quantity == 1

    @pytest.mark.unit
    def test_zero_quantity_raises_error(self):
        with pytest.raises(ValidationError):
            CartItem(product_id=1, quantity=0)

    @pytest.mark.unit
    def test_negative_quantity_raises_error(self):
        with pytest.raises(ValidationError):
            CartItem(product_id=1, quantity=-3)
