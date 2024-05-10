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