from fastapi import Request
from pydantic import BaseModel
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class CustomResponse(BaseModel):
    status_code: int
    status: str
    message: str
    data: list = None
    errors: list = None

class ValidationErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except RequestValidationError as e:
            custom_response = {
                "status_code": 400,
                "status": "Error",
                "message": "Dữ liệu không hợp lệ",
                "errors": [
                    {
                        "field": err["loc"][-1],
                        "message": err["msg"],
                        "input": err["input"]
                    } for err in e.errors()
                ]
            }
            return JSONResponse(status_code=400, content=custom_response)
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": f"Lỗi hệ thống: {str(e)}"})
