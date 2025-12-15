from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Input models
class ExampleInput(BaseModel):
    name: str
    value: str

class ExampleBody(BaseModel):
    input: ExampleInput

# Output model
class ExampleResponse(BaseModel):
    name: str
    value: str
    message: str = 'Success'

router = APIRouter(
    prefix="/example",
    tags=["example"]
)


@router.post("/process", response_model=ExampleResponse)
async def process_example(body: ExampleBody):
    """
    Example endpoint that processes input data.
    Replace this with your actual business logic.
    """
    try:
        name = body.input.name
        value = body.input.value
        
        # Your processing logic here
        processed_value = value.upper()
        
        return ExampleResponse(
            name=name,
            value=processed_value,
            message='Success'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_status():
    """Example GET endpoint"""
    return {"status": "operational"}
