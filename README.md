# pet-sitting-sitter-service

Sitter microservice for the pet-sitting platform. Manages sitter profiles,
service types, skills, calendar slots and capacity limits.

## Stack
- FastAPI + Uvicorn
- SQLAlchemy + pyodbc (Azure SQL Database)
- Pydantic v2
- Logging via stdlib `logging`

## Local run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

OpenAPI: <http://localhost:8001/docs>

## Configuration

Copy `.env.example` to `.env` (the real `.env` is gitignored
because GitHub push protection blocks Azure secrets):

```bash
cp .env.example .env
```

Default values used by the project:

```
DB_USERNAME=pasinozavr
DB_PASSWORD=61YcGTqd
DB_SERVER=tcp:cloud2026.database.windows.net
DB_DATABASE=pr2
ODBC_DRIVER=ODBC Driver 17 for SQL Server
LOG_LEVEL=INFO
```

## Endpoints
- `GET /health`
- `POST /init-db` — create `sitter` schema and tables
- `POST /seed` — insert stub data
- `GET /sitters`, `GET /sitters/{id}`, `POST /sitters`
- `GET /services`
- `GET /calendar-slots`

## Tests

```bash
pip install pytest flake8
flake8 app tests --max-line-length=120
pytest tests -v
```

## CI

`.github/workflows/ci.yml` runs `flake8` (static analysis) and `pytest`
(unit tests) on every push and pull request.

## Docker

```bash
docker build -t sitter-service .
docker run --rm -p 8001:8000 --env-file .env sitter-service
```
