from typing import Optional, List, Any
from pydantic import BaseModel 

class PaginationParams(BaseModel):
    page: Optional[int] = 1
    limit: Optional[int] = 20


class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    limit: int
    total_pages: int


def paginate(query, page: int = 1, limit: int = 20):
    total = query.count()
    offset = (page - 1) * limit
    items = query.offset(offset).limit(limit).all()
    total_pages = (total + limit - 1) // limit 
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages
    }
