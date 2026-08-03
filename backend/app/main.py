from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.api import api_router
from app.core.exceptions import AppError

app = FastAPI(title="POS-Lite API")


@app.exception_handler(AppError)
def handle_app_error(request: Request, exc: AppError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.get("/")
def root():
    return {"message": "POS-Lite API is running"}


app.include_router(api_router, prefix="/api")