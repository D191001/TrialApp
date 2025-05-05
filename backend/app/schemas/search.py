from typing import List, Optional

from pydantic import BaseModel

from .user import Gender


class SearchParams(BaseModel):
    gender: Optional[Gender] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    distance: Optional[float] = None
    interests: Optional[List[str]] = None


class UserSearchResult(BaseModel):
    id: int
    name: str
    age: int
    gender: Gender
    distance: float
    interests: List[str]
