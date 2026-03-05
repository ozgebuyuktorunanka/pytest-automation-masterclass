# 🧪 pytest-automation-masterclass
A hands-on Python test automation project built from scratch — covering Unit, API, and E2E testing with a production-grade architecture.

## 🔍 About
This repository is a structured, phase-based deep dive into Python test 
automation architecture. Built on top of a mock FastAPI application, it 
demonstrates how to design a scalable test suite from scratch — following 
the test pyramid principle with clear separation between unit, API, and 
E2E layers.

Each phase introduces a new layer of complexity: from pytest fundamentals 
and fixture scoping, to Page Object Model implementation with Playwright, 
Allure-based reporting pipelines, and GitHub Actions CI/CD integration.

Designed for engineers transitioning from JavaScript/Playwright ecosystems 
who want to build production-ready Python test infrastructure with best 
practices baked in from day one.

> Built as a learning repo for developers transitioning from JavaScript/Playwright to Python test automation.
---
## 🗺️ Roadmap

| Phase | Topic | Status |
|-------|-------|--------|
| 1 | Project Setup, Virtual Environment, pytest basics | ✅ Done |
| 2 | `parametrize`, Faker, advanced fixtures | 🔄 In Progress |
| 3 | API Testing with `httpx` + TestClient | ⏳ Planned |
| 4 | UI/E2E with Playwright Python + Page Object Model | ⏳ Planned |
| 5 | Fixture & Conftest architecture deep dive | ⏳ Planned |
| 6 | Reporting — Allure & pytest-html | ⏳ Planned |
| 7 | CI/CD — GitHub Actions | ⏳ Planned |

---

## 🏗️ Project Structure

```
pytest-automation-masterclass/
├── app/                        # Target system (FastAPI mock)
│   ├── __init__.py
│   ├── main.py                 # API endpoints (users, products, cart)
│   ├── models.py               # Pydantic models (validation)
│   └── database.py             # In-memory DB + reset utility
│
├── tests/
│   ├── conftest.py             # Global fixtures (setup/teardown)
│   ├── unit/
│   │   └── test_models.py      # Pydantic model validation tests
│   ├── api/
│   │   └── test_users_api.py   # HTTP endpoint tests
│   ├── e2e/                    # UI tests (Phase 4)
│   └── pages/                  # Page Object Models (Phase 4)
│
├── reports/                    # Test output reports
├── .github/
│   └── workflows/              # CI/CD (Phase 7)
├── pytest.ini                  # Central pytest configuration
└── requirements.txt
```

---

## ⚡ Quick Start

### Requirements
- Python 3.12+
- pip

### Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/pytest-automation-masterclass.git
cd pytest-automation-masterclass

# Create virtual environment
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
# .venv\Scripts\activate        # Windows

# Install dependencies
pip install -r requirements.txt
```

### Run Tests

```bash
# All tests
python -m pytest

# Verbose output
python -m pytest -v

# By folder
python -m pytest tests/unit/ -v
python -m pytest tests/api/ -v

# By marker
python -m pytest -m unit -v
python -m pytest -m api -v
python -m pytest -m smoke -v

# HTML report
python -m pytest --html=reports/report.html --self-contained-html
```

---

## 🧠 Key Concepts (Phase 1)

### conftest.py — The Heart of pytest

Fixtures defined here are **automatically available** to all tests — no import needed.
Think of it as a global `beforeEach` / `afterAll` but much more powerful.

```python
@pytest.fixture(autouse=True)   # runs before every test automatically
def reset_database():
    reset_db()                  # SETUP
    yield                       # ← test runs here
                                # TEARDOWN (add cleanup code here if needed)
```

### Fixture Scopes

| Scope | Runs | JS Equivalent |
|-------|------|---------------|
| `function` | Before every test (default) | `beforeEach` |
| `class` | Once per test class | — |
| `module` | Once per `.py` file | — |
| `session` | Once for the entire suite | `beforeAll` |

### Markers — Selective Test Execution

Defined in `pytest.ini`, used to run subsets of tests:

```bash
pytest -m smoke              # critical path only
pytest -m "not slow"         # skip slow tests
pytest -m "api and not smoke"  # combine markers
```

### Test Pyramid

```
      /\
     /E2E\         ← few  (slow, brittle, expensive)
    /──────\
   /  API   \      ← moderate
  /──────────\
 /    Unit    \    ← many  (fast, isolated, cheap)
──────────────
```

---

## 🔄 JS/Playwright → Python/pytest Cheatsheet

| JavaScript | Python |
|------------|--------|
| `describe()` | `class TestSomething:` |
| `it()` / `test()` | `def test_something():` |
| `beforeEach()` | `@pytest.fixture(autouse=True)` |
| `afterAll()` | code after `yield` with `scope="session"` |
| `expect(x).toBe(y)` | `assert x == y` |
| `expect(fn).toThrow()` | `with pytest.raises(ErrorType):` |
| `test.tag('@smoke')` | `@pytest.mark.smoke` |
| `@faker-js/faker` | `faker` library |
| `node_modules` + `package.json` | `.venv` + `requirements.txt` |
| TypeScript interfaces | Pydantic models |

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `fastapi` | Mock API (target system) |
| `uvicorn` | ASGI server |
| `pydantic` | Data validation (like Zod/TypeScript) |
| `pytest` | Test runner |
| `httpx` | HTTP client for API tests |
| `pytest-asyncio` | Async test support |
| `pytest-html` | Simple HTML reports |
| `allure-pytest` | Advanced reporting (Phase 6) |
| `faker` | Fake data generation |
| `python-dotenv` | `.env` file support |

---

## 📝 License

MIT