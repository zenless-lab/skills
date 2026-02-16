## FastAPI Backend Project Layout (Modular)

### Directory Structure

```
project_root/
├── pyproject.toml       # Project metadata and dependencies
├── alembic.ini          # Database migration configuration
├── Dockerfile           # Containerization instructions
├── app/                 # Application root directory
│   ├── __init__.py
│   ├── main.py          # FastAPI entry point (app = FastAPI())
│   ├── core/            # Core configuration
│   │   ├── config.py    # Pydantic Settings
│   │   └── security.py  # JWT/Authentication logic
│   ├── api/             # Route definitions
│   │   ├── __init__.py
│   │   ├── deps.py      # Dependency injection (Dependencies)
│   │   └── v1/          # Versioned API routes
│   │       ├── api.py   # Router aggregator
│   │       └── endpoints/
│   │           ├── users.py
│   │           └── items.py
│   ├── schemas/         # Pydantic models (Data Transfer Objects)
│   │   ├── item.py
│   │   └── user.py
│   ├── models/          # ORM models (SQLAlchemy/SQLModel)
│   │   ├── item.py
│   │   └── user.py
│   ├── crud/            # CRUD operations (Create, Read, Update, Delete)
│   │   ├── crud_item.py
│   │   └── crud_user.py
│   └── services/        # External service integrations (optional)
└── tests/               # Pytest test suite
    ├── conftest.py      # Test fixtures
    └── api/             # API integration tests

```

### Implementation Rules

1. **Entry Point**: Use `main.py` only for initializing the FastAPI app, configuring CORS/Middleware, and registering routers. Keep business logic out of this file.
2. **Separation of Concerns**:
    * **Schemas**: Define only the JSON structure for Requests and Responses.
    * **Models**: Define only the database table structures and relationships.
    * **CRUD**: Contain isolated database interaction code; do not include HTTP-specific logic.
    * **API/Endpoints**: Handle HTTP requests/responses by calling CRUD and Services.
3. **Dependency Injection**: Use FastAPI’s `Depends` for shared logic such as database sessions, current user validation, and security checks.
4. **API Versioning**: Group routes under versioned prefixes (e.g., `/api/v1`) to ensure backward compatibility.
5. **Environment Management**: Use Pydantic `BaseSettings` in `core/config.py` to manage environment variables and secrets.
