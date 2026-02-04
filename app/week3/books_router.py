from typing import Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException

books_router = APIRouter(prefix="/books", tags=["books"])


class Book(BaseModel):
    id: int
    title: str
    author: str
    price: int
    stock: int


books = [
    Book(id=1, title="Clean Code", author="Robert Martin", price=30000, stock=10),
    Book(id=2, title="Python Crash Course", author="Eric Matthes", price=25000, stock=5),
    Book(id=3, title="Deep Learning", author="Ian Goodfellow", price=45000, stock=3),
]


class BookCreate(BaseModel):
    title: str = Field(..., example="The Pragmatic Programmer")
    author: str = Field(..., example="Andrew Hunt")
    price: int = Field(..., ge=0, example=35000)
    stock: int = Field(..., ge=0, example=7)


class BookUpdate(BaseModel):
    title: str
    author: str
    price: int = Field(..., ge=0)
    stock: int = Field(..., ge=0)


class BookPatch(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[int] = Field(None, ge=0)
    stock: Optional[int] = Field(None, ge=0)


@books_router.get('', summary="도서 목록 조회")
def get_books():
    return books


@books_router.get(
    '/{book_id}',
    responses={404: {"description": "Book not found"}},
    summary="도서 단일 조회"
)
def get_book_by_id(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@books_router.post('', status_code=201, summary="도서 생성")
def create_book(payload: BookCreate):
    book = Book(id=len(books) + 1, **payload.model_dump())
    books.append(book)
    return book


@books_router.put(
    '/{book_id}',
    responses={404: {"description": "Book not found"}},
    summary="도서 전체 수정"
)
def update_book(book_id: int, payload: BookUpdate):
    for i, book in enumerate(books):
        if book.id == book_id:
            books[i] = Book(id=book_id, **payload.model_dump())
            return books[i]
    raise HTTPException(status_code=404, detail="Book not found")


@books_router.patch(
    '/{book_id}',
    responses={404: {"description": "Book not found"}},
    summary="도서 부분 수정"
)
def patch_book(book_id: int, payload: BookPatch):
    for book in books:
        if book.id == book_id:
            if payload.title is not None:
                book.title = payload.title
            if payload.author is not None:
                book.author = payload.author
            if payload.price is not None:
                book.price = payload.price
            if payload.stock is not None:
                book.stock = payload.stock
            return book

    raise HTTPException(status_code=404, detail="Book not found")


@books_router.delete(
    '/{book_id}',
    status_code=204,
    responses={404: {"description": "Book not found"}},
    summary="도서 삭제"
)
def delete_book(book_id: int):
    for book in books:
        if book.id == book_id:
            books.remove(book)
            return
    raise HTTPException(status_code=404, detail="Book not found")