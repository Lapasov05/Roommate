from datetime import date

from pydantic import BaseModel


class User_Phone(BaseModel):
    phone: str

class UserData(BaseModel):
    University:int
    faculty: int
    grade: int
    region: int
    district:int
    password1:str
    password2:str


class UserData_2(BaseModel):
    university: int
    faculty: int
    degree: int
    region: int
    district: int

class UserLogin(BaseModel):
    phone:str
    password:str