# ShortLink API

A containerized URL-shortening REST API built with **FastAPI, SQLAlchemy, SQLite, and Docker**.

ShortLink API converts long URLs into unique short codes, stores them persistently, and redirects users to the original URL through those codes.

## Features

- Create shortened URLs
- Generate unique 6-character short codes
- Persist URLs with SQLite and SQLAlchemy
- Redirect short codes to original URLs
- Return `404 Not Found` for invalid short codes
- Health-check endpoint
- Dockerized application
- Git/GitHub version control

## Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.12** | Application development |
| **FastAPI** | REST API framework |
| **Pydantic** | Request validation |
| **SQLAlchemy** | ORM and database interaction |
| **SQLite** | Persistent data storage |
| **shortuuid** | Unique short-code generation |
| **Uvicorn** | ASGI application server |
| **Docker** | Containerization |
| **Git & GitHub** | Version control and source management |

## Project Structure

    shortlink-api/
    ├── app/
    │   ├── __init__.py
    │   ├── database.py
    │   ├── main.py
    │   └── models.py
    ├── tests/
    │   └── __init__.py
    ├── .dockerignore
    ├── .gitignore
    ├── Dockerfile
    ├── requirements.txt
    ├── LICENSE
    └── README.md

> `shortlink.db` is generated at runtime and excluded from version control through `.gitignore`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Check API health |
| `POST` | `/shorten` | Create a shortened URL |
| `GET` | `/{short_code}` | Redirect to the original URL |

### Create a Short URL

    curl -X POST http://127.0.0.1:8000/shorten \
      -H "Content-Type: application/json" \
      -d '{"url":"https://www.example.com"}'

Example response:

    {
      "original_url": "https://www.example.com",
      "short_code": "aB12cD"
    }

### Follow a Short URL

    curl -v http://127.0.0.1:8000/aB12cD

The API returns a `307 Temporary Redirect` to the original URL.

### Health Check

    curl http://127.0.0.1:8000/health

Response:

    {
      "status": "healthy"
    }

## Local Setup

### 1. Clone the Repository

    git clone https://github.com/rahimahisah17/shortlink-api.git
    cd shortlink-api

### 2. Create a Virtual Environment

    python3 -m venv .venv

### 3. Activate the Virtual Environment

    source .venv/bin/activate

### 4. Install Dependencies

    pip install -r requirements.txt

### 5. Start the API

    uvicorn app.main:app --reload

The API will be available at:

    http://127.0.0.1:8000

### 6. Test the API

    curl http://127.0.0.1:8000/health

Expected response:

    {
      "status": "healthy"
    }

## Docker

The application is containerized using Docker for consistent development and deployment environments.

### Build the Image

    docker build -t shortlink-api:latest .

### Run the Container

    docker run -d \
      --name shortlink-api \
      -p 8000:8000 \
      shortlink-api:latest

### Check the Container

    docker ps

### Test the Containerized API

    curl http://127.0.0.1:8000/health

Expected response:

    {
      "status": "healthy"
    }

### View Container Logs

    docker logs shortlink-api

## Architecture

    Client
       │
       │ HTTP
       ▼
    FastAPI API :8000
       │
       ├── POST /shorten
       │
       └── GET /{short_code}
                │
                ▼
           SQLAlchemy ORM
                │
                ▼
             SQLite
          shortlink.db

### Request Flow

1. A client submits a long URL to `POST /shorten`.
2. FastAPI validates the request using Pydantic.
3. A unique short code is generated using `shortuuid`.
4. SQLAlchemy persists the URL and short code in SQLite.
5. The API returns the generated short code.
6. When the short code is requested, the API retrieves the original URL.
7. FastAPI returns a `307 Temporary Redirect` to the original URL.

> SQLite is used for the current MVP. The application can be evolved toward a production database such as PostgreSQL.

## Testing

The API has been manually validated locally and inside a Docker container using `curl`.

### Verified

- Health endpoint returns `200 OK`
- URL shortening returns a unique short code
- Shortened URLs are persisted in SQLite
- Short codes redirect to their original URLs
- Invalid short codes return `404 Not Found`
- Dockerized API starts successfully
- Dockerized `/health`, `/shorten`, and redirect endpoints respond successfully

Automated testing with `pytest` is planned as a future improvement.

## Current Limitations

This project is currently an MVP and has several areas for improvement:

- SQLite is suitable for development but not ideal for production-scale workloads.
- Authentication and authorization are not implemented.
- No URL expiration or custom aliases.
- No click analytics or usage tracking.
- No rate limiting or abuse protection.
- Automated test coverage has not yet been implemented.
- No CI/CD pipeline has been configured.
- The application has not yet been deployed to a cloud environment.

## Roadmap

- [ ] Add automated tests with `pytest`
- [ ] Improve request and response validation
- [ ] Improve error handling
- [ ] Add environment-based configuration
- [ ] Introduce PostgreSQL
- [ ] Add Docker Compose
- [ ] Add authentication and authorization
- [ ] Add URL expiration and custom aliases
- [ ] Add click analytics
- [ ] Add rate limiting
- [ ] Implement GitHub Actions CI/CD
- [ ] Deploy to Azure
- [ ] Add application monitoring and logging

## License

This project is licensed under the [MIT License](LICENSE).

## Author

**Rahimah Adufemi Sulayman**

Cloud & DevOps Engineer | Azure | Kubernetes | Docker | Python

- GitHub: [@rahimahisah17](https://github.com/rahimahisah17)
- Project Repository: [ShortLink API](https://github.com/rahimahisah17/shortlink-api)