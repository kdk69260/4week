from fastapi import FastAPI

from app.week3.items_router import items_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(items_router)
