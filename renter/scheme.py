from typing import Optional

from pydantic import BaseModel

from auth.scheme import RenterData_info


class Rent_scheme(BaseModel):
    name:str
    description:str
    room_count:int
    total_price:float
    student_jins_id:int
    student_count:int
    category_id:int
    location:str
    contract:bool
    longitude:float
    latitude:float
    wifi:bool
    conditioner:bool
    washing_machine:bool
    TV:bool
    refrigerator:bool
    furniture:bool
    other_convenience:str


# class Update_rent(BaseModel):
#     student_jins_id: Optional[int] = None
#     name: Optional[str] = None
#     description: Optional[str] = None
#     room_count: Optional[int] = None
#     total_price: Optional[float] = None
#     student_count: Optional[int] = None
#     category_id: Optional[int] = None
#     location: Optional[str] = None
#     contract: Optional[bool] = None
#     longitude: Optional[float] = None
#     latitude: Optional[float] = None
#     wifi: Optional[bool] = None
#     conditioner: Optional[bool] = None
#     washing_machine: Optional[bool] = None
#     TV: Optional[bool] = None
#     refrigerator: Optional[bool] = None
#     furniture: Optional[bool] = None
#     other_convenience: Optional[str] = None

class My_rent_scheme(BaseModel):
    id:int
    name:str
    description:str
    room_count:int
    total_price:float
    student_jins_id:int
    renter_id:RenterData_info
    student_count:int
    contract:bool
    category_id:int
    location:str
    longitude:float
    latitude:float
    wifi:bool
    conditioner:bool
    washing_machine:bool
    TV:bool
    refrigerator:bool
    furniture:bool
    other_convenience:str