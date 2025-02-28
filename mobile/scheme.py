from typing import Union, List

from pydantic import BaseModel, Field

from auth.scheme import UserData_info


class CategoryScheme(BaseModel):
    id: int
    name_uz: str
    name_ru: str


class JinsScheme(BaseModel):
    id: int
    name_uz: str
    name_ru: str


class RenterInfoScheme(BaseModel):
    id: int
    firstname: str
    lastname: str
    phone: str
    image: str


class RentImageScheme(BaseModel):
    id: int
    url: str
    hashcode: str


class RentGETScheme(BaseModel):
    id: int
    name: str
    description: str
    category: CategoryScheme
    room_count: int
    total_price: float
    jins: JinsScheme
    image: List[RentImageScheme]
    student_count: int
    renter: RenterInfoScheme
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


class ReviewPostScheme(BaseModel):
    rent_id: int
    rate: int = Field(gte=0, lte=5)
    comment: Union[str, None]


class UserInfo(BaseModel):
    id: int
    firstname: Union[str, None]
    lastname: Union[str, None]
    phone: Union[str, None]
    image: Union[str, None]


class RateGetScheme(BaseModel):
    id: int
    rate: int
    rent_id: int
    comment: str
    user: UserInfo


class RentScheme(BaseModel):
    id: int
    name: str
    description: str
    category: CategoryScheme
    room_count: int
    total_price: float
    student_count: int
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


class WishlistGETScheme(BaseModel):
    id: int
    rent: RentScheme


class AnnouncementPOSTScheme(BaseModel):
    title: str
    description: str
    type_id: int



#========================================================

class UniversityCreate(BaseModel):
    name_uz: str
    name_ru: str
    acronym_uz: str
    acronym_ru: str
    longitude: float
    latitude: float

class FacultyCreate(BaseModel):
    name_uz: str
    name_ru: str
    university_id: int
    longitude: float
    latitude: float