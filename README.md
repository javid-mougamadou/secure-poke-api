# SecurePokeAPI

## Run the project

```bash
docker compose up -d --build
```

Then populate the types (once `access-management-api` is up):

```bash
docker compose exec access-management-api uv run python manage.py populate_types
```

## Routes

### `access-management-api` (`http://localhost:8000`)

| Method | Route | Auth | Body |
|---|---|---|---|
| `POST` | `/api/login/` | — | `{"username": "...", "password": "..."}` |
| `POST` | `/api/group/<type>/add/` | `Bearer <token>` | — |
| `POST` | `/api/group/<type>/remove/` | `Bearer <token>` | — |
| `GET` | `/api/user/me/` | `Bearer <token>` | — |

### `get-them-all-api` (`http://localhost:8001`)

| Method | Route | Auth |
|---|---|---|
| `GET` | `/api/pokemon/` | `Bearer <token>` |
| `GET` | `/api/pokemon/<id or name>/` | `Bearer <token>` |

The token is the one obtained via `/api/login/` on `access-management-api`, forwarded as-is to both APIs.

## Documentation (Swagger / Redoc)

| API | Redoc |
|---|---|
| `access-management-api` | http://localhost:8000/redoc/ |
| `get-them-all-api` | http://localhost:8001/redoc/ |

> `/swagger.json` is currently broken (404) on both APIs — only `/redoc/` works.

## Tests

```bash
docker compose exec access-management-api uv run pytest
docker compose exec get-them-all-api uv run pytest
```
