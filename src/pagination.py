from typing import Optional, List, Generic, TypeVar
from pydantic import BaseModel 


T = TypeVar("T")


class PaginationParams(BaseModel):
    page: Optional[int] = 1
    limit: Optional[int] = 20


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    limit: int
    total_pages: int


def paginate(query, schema, page: int = 1, limit: int = 20):
    total = query.count()
    offset = (page - 1) * limit
    records = query.offset(offset).limit(limit).all()
    items = [schema.model_validate(r) for r in records]
    total_pages = (total + limit - 1) // limit 
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages
    }