from fastapi import FastAPI

from app.week3.books_router import books_router
from app.week4.user_router import user_router
from app.week4.database import create_db_and_tables

app = FastAPI()

create_db_and_tables()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(books_router)
app.include_router(user_router)
