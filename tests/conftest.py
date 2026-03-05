"""
conftest.py — pytest
  - beforeAll / afterAll  →  scope="session"
  - beforeEach / afterEach →  scope="function" (default)

conftest.py:
  - The fixtures in this file are automatically visible to ALL tests
  - No need to import them, pytest finds them automatically
  - Nested conftest.py files are possible (folder-based overrides)
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import reset_db


# ──────────────────────────────────────────────────────
# WHAT IS SCOPE?
#
#  "function"  → Runs before/after each test function (default)
#  "class"     → Runs before/after each test class
#  "module"    → Runs before/after each .py file
#  "session"   → Runs before/after the entire test suite (once)
# ──────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def api_client():
    """
    FastAPI TestClient — session boyunca tek instance.

    JS Playwright'taki:
      test.use({ baseURL: 'http://localhost:3000' })
    gibi düşün, ama çok daha güçlü.

    httpx tabanlı, gerçek HTTP request'i simüle eder.
    """
    with TestClient(app) as client:
        yield client
    # yield'dan sonraki kod → teardown (afterAll)


@pytest.fixture(autouse=True)
def reset_database():
    """
    autouse=True → Her teste otomatik uygulanır, çağırmana gerek yok.

    Bu fixture test izolasyonu sağlar:
    Her test temiz bir DB ile başlar.

    JS Playwright'taki:
      test.beforeEach(async () => { await resetDB() })
    karşılığı.
    """
    reset_db()   # setup: runs before test 
    yield        # ← runs here in test.
    # teardown: runs after test.


@pytest.fixture
def sample_user():
    """User Data Sample. We will use this information in tests."""
    return {"id": 99, "name": "Test User", "email": "test@example.com", "age": 28}


@pytest.fixture
def sample_product():
    """Product Data Sample for test"""
    return {"id": 99, "name": "Test Product", "price": 49.99, "stock": 5}
