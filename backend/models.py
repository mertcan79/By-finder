from pydantic import BaseModel, Field
from datetime import datetime as dt
from typing import Union, Any, Optional

class Flat(BaseModel):
    id: str 
    price: float
    rooms: int
    distance: str
    quality: float

class SearchParams(BaseModel):
    price: Optional[float]
    rooms: Optional[int]
    quality: Optional[int]
    sqfts: Optional[float]
    
class Coordinate(BaseModel):
    latitude: float
    longitude: float