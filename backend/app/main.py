from fastapi import FastAPI

from app.api.api import api_router

app = FastAPI(title="POS-Lite API")


@app.get("/")
def root():
    return {"message": "POS-Lite API is running"}


app.include_router(api_router, prefix="/api")