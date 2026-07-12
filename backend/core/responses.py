from typing import Any, Optional
from fastapi.responses import JSONResponse

def success_response(data: Any = None, message: str = "Request processed successfully.", status_code: int = 200) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": data
        }
    )

def error_response(message: str = "An error occurred.", errors: Optional[Any] = None, status_code: int = 400) -> JSONResponse:
    content = {
        "success": False,
        "message": message
    }
    if errors is not None:
        content["errors"] = errors
    return JSONResponse(
        status_code=status_code,
        content=content
    )
