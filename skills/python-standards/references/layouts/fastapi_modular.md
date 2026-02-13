# FastAPI Modular Layout (Scalable)

## Overview
Designed for larger web APIs, separating concerns into routers, schemas (Pydantic), and database models (ORM).

## Directory Tree
```text
project_root/
├── app/
│   ├── main.py           # App initialization
│   ├── dependencies.py   # Global dependencies (auth, etc.)
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── items.py
│   ├── internal/         # Admin/Internal logic
│   │   └── admin.py
│   ├── models/           # DB ORM Classes (SQLAlchemy)
│   └── schemas/          # Pydantic Models (Request/Response)
├── alembic/              # DB Migrations
└── tests/
    └── test_api.py
```

## Best Practices

* Use `APIRouter` in `routers/*.py` files.
* Include routers in `app/main.py` using `app.include_router()`.
