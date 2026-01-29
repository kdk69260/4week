from typing import Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException

items_router = APIRouter(prefix="/items", tags=["items"])

class Item(BaseModel):
    id: int
    data: str
    price: int

items = [
    Item(id=1, data='apple', price=500),
    Item(id=2, data='banana', price=1000),
    Item(id=3, data='cherry', price=800),
]

class ItemCreate(BaseModel):
    data: str = Field(..., example="orange")
    price: int = Field(..., ge=0, example=1200)

class ItemUpdate(BaseModel):
    data: str
    price: int = Field(..., ge=0)

class ItemPatch(BaseModel):
    data: Optional[str] = None
    price: Optional[int] = Field(None, ge=0)


@items_router.get(
    '',
    status_code=200,
    summary="아이템 목록 조회"
)
def get_items():
    return items


@items_router.get(
    '/{item_id}',
    status_code=200,
    responses={404: {"description": "Item not found"}},
    summary="아이템 단일 조회"
)
def get_item_by_id(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail='Item not found')


@items_router.post(
    '',
    status_code=201,
    summary="아이템 생성"
)
def create_item(payload: ItemCreate):
    item = Item(id=len(items)+1, **payload.model_dump())
    items.append(item)
    return item


@items_router.put(
    '/{item_id}',
    status_code=200,
    responses={404: {"description": "Item not found"}},
    summary="아이템 전체 수정"
)
def update_item(item_id: int, payload: ItemUpdate):
    for item in items:
        if item.id == item_id:
            item = Item(id=item_id, **payload.model_dump())
            return item
    raise HTTPException(status_code=404, detail='Item not found')


@items_router.patch(
    '/{item_id}',
    status_code=200,
    responses={404: {"description": "Item not found"}},
    summary="아이템 부분 수정"
)
def patch_item(item_id: int, payload: ItemPatch):
    for item in items:
        if item.id == item_id:
            if payload.data is not None:
                item.data = payload.data
            if payload.price is not None:
                item.price = payload.price
            return item
    raise HTTPException(status_code=404, detail='Item not found')


@items_router.delete(
    '/{item_id}',
    status_code=204,
    responses={404: {"description": "Item not found"}},
    summary="아이템 삭제"
)
def delete_item(item_id: int):
    for item in items:
        if item.id == item_id:
            items.remove(item)
            return
    raise HTTPException(status_code=404, detail='Item not found')
