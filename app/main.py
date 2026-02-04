from fastapi import FastAPI

from app.week3.books_router import books_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(books_router)
