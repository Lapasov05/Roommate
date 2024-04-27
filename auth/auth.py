import secrets
from datetime import date, datetime

import aiofiles
from fastapi import APIRouter, HTTPException, UploadFile, Depends
from sqlalchemy import select, insert
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from database import get_async_session
from .scheme import User_Phone, UserData, UserLogin
from models.models import User, Renter
from .utils import generate_token

auth_router = APIRouter()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

user_data = {}  # Initialize user_data dictionary


@auth_router.post('/phone_number')
async def phone_number(user_phone: User_Phone, session: AsyncSession = Depends(get_async_session)):
    try:
        query_phone = select(User).where(User.phone == user_phone.phone)
        query_phone_renter = select(Renter).where(Renter.phone == user_phone.phone)
        result = await session.execute(query_phone)
        result_renter = await session.execute(query_phone_renter)

        if not result and result_renter:
            return HTTPException(status_code=400, detail="Phone already used!")
        else:
            user_data['phone'] = user_phone.phone
            print(user_data)
            return HTTPException(status_code=200, detail="Message sent!")

    except Exception as e:
        return HTTPException(status_code=500, detail=f"{e}")


@auth_router.post('/phone_number/sms')
async def get_sms(message: int):
    if message == 1234:
        return HTTPException(status_code=200, detail="Correct code!")
    else:
        return HTTPException(status_code=400, detail="Wrong code!")


@auth_router.post('/register/student/step_1')
async def register_user(image: UploadFile,
                        first_name: str,
                        last_name: str,
                        gender: int,
                        invisible: bool,
                        birth_date: date,
                        session: AsyncSession = Depends(get_async_session)):
    try:
        name = image.filename
        out_file = f'images/{name}'
        async with aiofiles.open(out_file, 'wb') as zipf:
            content = await image.read()
            await zipf.write(content)
        hashcode = secrets.token_hex(32)
        user_data.update({  # Update user_data dictionary with new data
            'image': hashcode,
            'first_name': first_name,
            'last_name': last_name,
            'gender': gender,
            'invisible': invisible,
            'birth_date': birth_date
        })
        return HTTPException(status_code=200, detail="Saved!")
    except Exception as e:
        return HTTPException(status_code=500, detail=f"{e}")


@auth_router.post('/register/student/step_2')
async def register_step2(user: UserData, session: AsyncSession = Depends(get_async_session)):
    if user.password1 == user.password2:
        try:
            print(user_data)
            password_hash = pwd_context.hash(user.password2)
            query = insert(User).values(
                firstname=user_data['first_name'],  # Use data from user_data
                lastname=user_data['last_name'],  # Use data from user_data
                phone=user_data['phone'],  # Use data from user_data
                jins_id=user_data['gender'],
                university_id=user.University,
                faculty_id=user.faculty,
                grade=user.grade,
                password=password_hash,
                image=user_data['image'],  # Use data from user_data
                invisible=user_data['invisible'],  # Use data from user_data
                district_id=user.district,
                register_at=datetime.utcnow()
            )
            await session.execute(query)
            await session.commit()
            return HTTPException(status_code=200, detail="Registered")
        except Exception as e:
            return HTTPException(status_code=500, detail=f"{e}")
    else:
        return HTTPException(status_code=400, detail="Passwords are not the same!")


@auth_router.post('/register/renter')
async def register_user_student(image: UploadFile,
                                first_name: str,
                                last_name: str,
                                password_1: str,
                                password_2: str,
                                session: AsyncSession = Depends(get_async_session)):
    try:
        if password_1 == password_2:
            password_hash = pwd_context.hash(password_2)
            name = image.filename
            out_file = f'images/{name}'
            async with aiofiles.open(out_file, 'wb') as zipf:
                content = await image.read()
                await zipf.write(content)
            hashcode = secrets.token_hex(32)
            query = insert(Renter).values(firstname=first_name,
                                          lastname=last_name,
                                          phone=user_data['phone'],
                                          password=password_hash,
                                          image=hashcode,
                                          register_at=datetime.utcnow())
            await session.execute(query)
            await session.commit()
            return HTTPException(status_code=200, detail="Registered!")
        else:
            return HTTPException(status_code=400, detail="Passwords are not same!")
    except Exception as e:
        return HTTPException(status_code=400, detail=f"{e}")


@auth_router.post('/login/Student')
async def login(user: UserLogin, session: AsyncSession = Depends(get_async_session)):
    try:
        query_user = select(User).where(User.phone == user.phone)

        res_user = await session.execute(query_user)

        user_result = res_user.scalar_one_or_none()

        if user_result and pwd_context.verify(user.password, user_result.password):
            token = generate_token(user_result.id)
            print('User')
            return {"status_code": 200, "detail": token}
        else:
            return HTTPException(status_code=401, detail="Login Failed")
    except NoResultFound:
        return HTTPException(status_code=401, detail="User or Renter not found")
    except MultipleResultsFound:
        return HTTPException(status_code=500, detail="Multiple users or renters found")
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@auth_router.post('/login/Renter')
async def login(user: UserLogin, session: AsyncSession = Depends(get_async_session)):
    try:
        query_renter = select(Renter).where(Renter.phone == user.phone)

        res_renter = await session.execute(query_renter)

        renter_result = res_renter.scalar_one_or_none()

        if renter_result and pwd_context.verify(user.password, renter_result.password):
            token = generate_token(renter_result.id)
            print('Renter')
            return {"status_code": 200, "detail": token}
        else:
            return HTTPException(status_code=401, detail="Login Failed")
    except NoResultFound:
        return HTTPException(status_code=401, detail="User or Renter not found")
    except MultipleResultsFound:
        return HTTPException(status_code=500, detail="Multiple users or renters found")
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
