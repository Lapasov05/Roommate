from datetime import date

from pydantic import BaseModel


class User_Phone(BaseModel):
    phone: str

# class UserData(BaseModel):
#     firstname: str
#     lastname: str
#     phone:str
#     jins_id: int
#     password1:str
#     password2:str
#     invisible: bool


class RenterData(BaseModel):
    firstname: str
    lastname: str
    phone:str
    birth_date: date
    password1:str
    password2:str
    invisible: bool


class UserData_2(BaseModel):
    university_id: int
    faculty_id: int
    grade: int
    district_id: int

class UserLogin(BaseModel):
    phone:str
    password:str


class University_list(BaseModel):
    id:int
    name:str
    acronym:str
    longitude:float
    latitude:float

class faculty_list(BaseModel):
    id:int
    name:str
    university_id:int
    longitude:float
    latitude:float


class region_list(BaseModel):
    id: int
    name: str

class district_list(BaseModel):
    id: int
    name: str
    region_id:int