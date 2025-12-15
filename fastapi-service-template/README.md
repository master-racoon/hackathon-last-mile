# FastAPI Service Template

A production-ready FastAPI microservice template with Docker support.

## Features

- ✅ FastAPI with Pydantic v2
- ✅ Multi-stage Docker builds (dev & prod)
- ✅ UV package manager for fast installs
- ✅ Request/Response logging middleware
- ✅ Structured project layout (routers, services, repositories)
- ✅ SQLAlchemy integration ready
- ✅ OpenAI integration ready
- ✅ Environment-based configuration
- ✅ Health check endpoints

## Project Structure

```
fastapi-service-template/
├── app/
│   ├── main.py                  # Application entry point
│   ├── routers/                 # API route handlers
│   │   └── example.py
│   ├── services/                # Business logic
│   │   └── example_service.py
│   ├── repositories/            # Database access layer
│   │   └── example_repository.py
│   └── .env.example             # Environment variables template
├── Dockerfile.dev               # Development Docker image
├── Dockerfile.prod              # Production Docker image
├── requirements.txt             # Python dependencies
└── .dockerignore               # Docker ignore file
```

## Getting Started

### Local Development (with Docker)

1. **Copy environment variables**:

   ```bash
   cp app/.env.example app/.env.development.local
   # Edit app/.env.development.local with your values
   ```

2. **Add to docker-compose.yaml**:

   ```yaml
   your-service:
     build:
       context: ./fastapi-service-template
       dockerfile: Dockerfile.dev
     volumes:
       - ./fastapi-service-template/app:/usr/src/app
     ports:
       - "8000:8000"
     env_file:
       - ./fastapi-service-template/app/.env.development.local
     depends_on:
       - database
   ```

3. **Start the service**:

   ```bash
   docker-compose up your-service
   ```

4. **Access the API**:
   - API: http://localhost:8000
   - Swagger Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Local Development (without Docker)

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**:

   ```bash
   cp app/.env.example app/.env
   # Edit app/.env with your values
   ```

3. **Run the application**:
   ```bash
   cd app
   uvicorn main:app --reload --port 8000
   ```

## Creating New Endpoints

1. **Create a new router** in `app/routers/`:

   ```python
   from fastapi import APIRouter
   from pydantic import BaseModel

   router = APIRouter(prefix="/myrouter", tags=["myrouter"])

   @router.get("/")
   async def my_endpoint():
       return {"message": "Hello!"}
   ```

2. **Register the router** in `app/main.py`:

   ```python
   from routers.myrouter import router as myrouter

   app.include_router(myrouter)
   ```

## Adding Business Logic

- **Services**: Put business logic in `app/services/`
- **Repositories**: Put database access in `app/repositories/`
- **Models**: Create Pydantic models in your router files or a separate `models/` directory

## Environment Variables

Configure these in your `.env` file:

- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: OpenAI API key (if using)
- `HASURA_GRAPHQL_ENDPOINT`: Hasura GraphQL endpoint (if using)
- `HASURA_ADMIN_SECRET`: Hasura admin secret (if using)

## Production Deployment

Use `Dockerfile.prod` for production builds:

```bash
docker build -f Dockerfile.prod -t your-service:latest .
docker run -p 8080:8080 \
  -e DATABASE_URL="your_db_url" \
  -e OPENAI_API_KEY="your_key" \
  your-service:latest
```

## Dependencies

Core packages included:

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `sqlalchemy` - Database ORM
- `psycopg2` - PostgreSQL adapter
- `python-dotenv` - Environment variables
- `httpx` - HTTP client
- `openai` - OpenAI integration
- `beautifulsoup4` - HTML parsing

## License

MIT - Use this template however you like!
