from fastapi import FastAPI
app = FastAPI()

from .v1 import config

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
