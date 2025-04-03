from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from movie_service.app.main import app


class CustomResponse(BaseModel):
    status_code: int
    status: str
    message: str
    data: list = None
    errors: list = None


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    custom_response = {
        "status_code": 400,
        "status": "Error",
        "message": "Dữ liệu không hợp lệ",
        "errors": [
            {"field": err["loc"][-1], "message": err["msg"], "input": err["input"]}
            for err in exc.errors()
        ],
    }
    return JSONResponse(status_code=400, content=custom_response)
