# Agent Guideline – Folder Structure Reference

## Project Structure

### An outer module named apps which will contain all the django apps and project should strictly follow the below pattern

```
apps/
└── locations/
    ├── __init__.py
    ├── apps.py
    ├── urls.py
    │
    ├── api/                              # API Layer (Presentation)
    │   └── v1/
    │       ├── __init__.py
    │       ├── country.py               # Country endpoints GET, POST, PUT, PATCH, DELETE
    │       ├── emergency_location.py
    │       └── location_api.py
    │
    ├── repositories/                    # Data Access Layer
    │   ├── __init__.py
    │   ├── country_repository.py        # Country data access
    │   └── location_repository.py       # Location data access
    │
    ├── serializers/                     # Validation Layer
    │   ├── __init__.py
    │   ├── country_serializers.py       # Country DTOs
    │   ├── location_data_serializers.py
    │   └── location_serializers.py      # Location DTOs
    │
    ├── services/                        # Business Logic Layer
    │   ├── __init__.py
    │   ├── country_service.py           # Country business logic
    │   ├── emergency_location_service.py # Emergency location logic
    │   └── location_service.py          # Location business logic
    │
    ├── tasks/                           # Async Tasks
    │   ├── __init__.py
    │   └── emergency_location_tasks.py
    │
    └── tests/                           # Comprehensive Testing
        ├── __init__.py
        ├── integration/                 # Integration tests
        │   ├── __init__.py
        │   ├── conftest.py              # Integration fixtures
        │   ├── test_location_api_integration.py
        │   ├── test_location_repository_integration.py
        │   └── test_location_repository_with_fixtures.py
        ├── repositories/               # Repository unit tests
        │   ├── __init__.py
        │   ├── test_country_repository.py
        │   └── test_location_repository.py
        ├── services/                   # Service unit tests
        │   ├── __init__.py
        │   ├── test_country_service.py
        │   ├── test_emergency_location_service.py
        │   └── test_location_service.py
        ├── test_country_api.py         # API unit tests
        ├── test_emergency_location_api.py
        └── test_location_api.py
```

## Layer Responsibilities

### API Layer (`api/v1/`)
- HTTP endpoint handlers organised by resource
- Request validation and response formatting
- CRUD operations for locations, countries, and emergency locations

### Repository Layer (`repositories/`)
- Database access and query logic
- Abstracts ORM/raw SQL from business logic
- One repository per model/resource

### Serializer Layer (`serializers/`)
- Input validation and deserialization (DTOs in)
- Output serialization (DTOs out)
- Shared data-shape contracts between layers

### Service Layer (`services/`)
- Core business logic
- Orchestrates repositories and external integrations
- Keeps API and repository layers free of business rules

### Tasks Layer (`tasks/`)
- Async / background job definitions (e.g. Celery tasks)
- Triggered by services or scheduled workers

### Tests (`tests/`)
- `integration/` – end-to-end database/API integration tests with fixtures
- `repositories/` – unit tests for data access logic
- `services/` – unit tests for business logic
- Root-level `test_*_api.py` – unit tests for API handlers