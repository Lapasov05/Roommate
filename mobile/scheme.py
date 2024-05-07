from typing import Union

from pydantic import BaseModel, Field


class CategoryScheme(BaseModel):
    id: int
    name: str


class JinsScheme(BaseModel):
    id: int
    name: str


class RentGETScheme(BaseModel):
    id: int
    name: str
    description: str
    category: CategoryScheme
    room_count: int
    total_price: float
    jins: JinsScheme
    student_count: int
    renter_id: int
    location: str
    latitude: float
    longitude: float
    wifi: bool
    conditioner: bool
    washing_machine: bool
    TV: bool
    refrigerator: bool
    furniture: bool
    other_convenience: str


class RentADDScheme(BaseModel):
    name: str
    description: str
    category_id: int = Field(gt=0)
    room_count: int = Field(gt=0)
    total_price: float = Field(gte=0)
    student_jins_id: int = Field(gt=0)
    student_count: int = Field(gt=0)
    location: str
    latitude: float
    longitude: float
    wifi: bool = Field(default=False)
    conditioner: bool = Field(default=False)
    washing_machine: bool = Field(default=False)
    TV: bool = Field(default=False)
    refrigerator: bool = Field(default=False)
    furniture: bool = Field(default=False)
    other_convenience: str


class FilterScheme(BaseModel):
    from_price: Union[float, None]
    end_price: Union[float, None]
    rate: Union[int, None]
    range: Union[int, None]







