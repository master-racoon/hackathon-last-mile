from fastapi import FastAPI, Request, Response
from starlette.background import BackgroundTask
import logging
import json
from pathlib import Path

# Import your routers here
from routers.example import router as example_router

app = FastAPI(
    title="FastAPI Service Template",
    description="A template for creating FastAPI microservices",
    version="1.0.0"
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Include your routers here
app.include_router(example_router)


def log_info(req_body, res_body):
    """Log request and response information"""
    logging.info(f"Request: {req_body}")
    logging.info(f"Response: {res_body}")


async def set_body(request: Request, body: bytes):
    """Helper to set body on request object"""
    async def receive():
        return {'type': 'http.request', 'body': body}
    request._receive = receive


@app.middleware('http')
async def logging_middleware(request: Request, call_next):
    """Middleware to log all requests and responses"""
    req_body = await request.body()
    await set_body(request, req_body)
    response = await call_next(request)
    
    res_body = b''
    async for chunk in response.body_iterator:
        res_body += chunk
    
    task = BackgroundTask(log_info, req_body, res_body)
    return Response(
        content=res_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
        background=task
    )


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "service": "fastapi-service-template"}


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}


@app.on_event("startup")
async def save_openapi_spec():
    """Save OpenAPI specification to api.json on startup"""
    try:
        openapi_schema = app.openapi()
        output_path = Path(__file__).parent / "api.json"
        with open(output_path, "w") as f:
            json.dump(openapi_schema, f, indent=2)
        logging.info(f"OpenAPI specification saved to {output_path}")
    except Exception as e:
        logging.error(f"Failed to save OpenAPI specification: {e}")


@app.get("/api.json")
async def get_openapi_json():
    """Endpoint to retrieve the OpenAPI specification in JSON format"""
    return app.openapi()
