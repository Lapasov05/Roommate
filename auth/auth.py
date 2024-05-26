import secrets
from datetime import date, datetime
from typing import List

import aiofiles
from fastapi import APIRouter, HTTPException, UploadFile, Depends
from sqlalchemy import select, insert, update
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from database import get_async_session
from .scheme import User_Phone, UserLogin, UserData_2, University_list, faculty_list, district_list, region_list, \
    UserData_info, RenterData, RenterData_info, change_password
from models.models import User, Renter, University, Faculty, District, Region
from .utils import generate_token, verify_token, generate_token_renter

auth_router = APIRouter()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

user_data = {}  # Initialize user_data dictionary


@auth_router.post('/phone_number/')
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


@auth_router.put('/student/reset-password/')
async def reset_password(phone: str,
                         password_1: str,
                         password_2: str,
                         session: AsyncSession = Depends(get_async_session)):
    try:
        if password_1 == password_2:
            query = select(User).where(User.phone == phone)
            res = await session.execute(query)
            result = res.scalars().one_or_none()
            if result:
                hash_password = pwd_context.hash(password_2)
                query_update = update(User).where(User.phone == phone).values(password=hash_password)
                await session.execute(query_update)
                await session.commit()
                return HTTPException(status_code=200, detail="Password updated")
            else:
                raise HTTPException(status_code=400, detail="User does not exist")
        else:
            raise HTTPException(status_code=400, detail="Passwords do not match")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@auth_router.put('/renter/reset-password/')
async def reset_password(phone: str,
                         password_1: str,
                         password_2: str,
                         session: AsyncSession = Depends(get_async_session)):
    try:
        if password_1 == password_2:
            query = select(Renter).where(Renter.phone == phone)
            res = await session.execute(query)
            result = res.scalars().one_or_none()
            if result:
                hash_password = pwd_context.hash(password_2)
                query_update = update(Renter).where(Renter.phone == phone).values(password=hash_password)
                await session.execute(query_update)
                await session.commit()
                return HTTPException(status_code=200, detail="Password updated")
            else:
                raise HTTPException(status_code=400, detail="User does not exist")
        else:
            raise HTTPException(status_code=400, detail="Passwords do not match")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@auth_router.post('/phone_number/sms/')
async def get_sms(message: int):
    if message == 1234:
        return HTTPException(status_code=200, detail="Correct code!")
    else:
        return HTTPException(status_code=400, detail="Wrong code!")


@auth_router.post('/student/register/step_1/')
async def register_user(image: UploadFile,
                        firstname: str,
                        lastname: str,
                        phone: str,
                        jins_id: int,
                        password1: str,
                        password2: str,
                        invisible: bool,
                        session: AsyncSession = Depends(get_async_session)):
    try:
        if password1 == password2:
            name = image.filename
            out_file = f'images/{name}'
            async with aiofiles.open(out_file, 'wb') as zipf:
                content = await image.read()
                await zipf.write(content)
            hashcode = secrets.token_hex(32)
            hashed_password = pwd_context.hash(password2)
            query = insert(User).values(firstname=firstname,
                                        lastname=lastname,
                                        phone=phone,
                                        jins_id=jins_id,
                                        password=hashed_password,
                                        invisible=invisible,
                                        image=hashcode,
                                        register_at=datetime.utcnow())
            await session.execute(query)
            await session.commit()
            return HTTPException(status_code=200, detail="Saved!")
    except Exception as e:
        return HTTPException(status_code=500, detail=f"{e}")


@auth_router.put('/student/set-profile/')
async def set_profile(model: UserData_2,
                      token: dict = Depends(verify_token),
                      session: AsyncSession = Depends(get_async_session)
                      ):
    try:
        if token is not None:
            user_id = token.get('user_id')
            query = update(User).where(User.id == user_id).values(**dict(model))
            await session.execute(query)
            await session.commit()
            return HTTPException(status_code=200, detail="Updated")
        else:
            return HTTPException(status_code=400, detail="Invalid token")
    except Exception as e:
        return HTTPException(status_code=400, detail=f"{e}")


@auth_router.post('/renter/register/')
async def register_user_student(image: UploadFile,
                                first_name: str,
                                last_name: str,
                                phone: str,
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
                                          phone=phone,
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


@auth_router.post('/student/login/')
async def login(user: UserLogin, session: AsyncSession = Depends(get_async_session)):
    try:
        query_user = select(User).where(User.phone == user.phone)

        res_user = await session.execute(query_user)

        user_result = res_user.scalar_one_or_none()

        if user_result and pwd_context.verify(user.password, user_result.password):
            token = generate_token(user_result.id, user_result.jins_id)
            print('User')
            return {"status_code": 200, "detail": token}
        else:
            return HTTPException(status_code=401, detail="Login Failed")
    except NoResultFound:
        return HTTPException(status_code=401, detail="User or Renter not found")
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@auth_router.post('/renter/login/')
async def login(user: UserLogin, session: AsyncSession = Depends(get_async_session)):
    try:
        query_renter = select(Renter).where(Renter.phone == user.phone)

        res_renter = await session.execute(query_renter)

        renter_result = res_renter.scalar_one_or_none()

        if renter_result and pwd_context.verify(user.password, renter_result.password):
            token = generate_token_renter(renter_result.id)
            print('Renter')
            return {"status_code": 200, "detail": token}
        else:
            return HTTPException(status_code=401, detail="Login Failed")
    except NoResultFound:
        return HTTPException(status_code=401, detail="User or Renter not found")
    except MultipleResultsFound:
        return HTTPException(status_code=500, detail="Multiple users or renters found")
    # except Exception as e:
    #     return HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


@auth_router.get('/get_university/', response_model=List[University_list])
async def get_university(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(University)
        res = await session.execute(query)
        result = res.scalars().all()
        return result
    except Exception as e:
        return HTTPException(status_code=500, detail=f"{e}")


@auth_router.get('/get_faculty/', response_model=List[faculty_list])
async def get_faculty(university_id: int,
                      session: AsyncSession = Depends(get_async_session)
                      ):
    try:
        query = select(Faculty).where(Faculty.university_id == university_id)
        res = await session.execute(query)
        result = res.scalars().all()
        return result
    except Exception as e:
        return HTTPException(status_code=500, detail=f"{e}")


@auth_router.get('/get_region/', response_model=List[region_list])
async def get_regions(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Region)
        res = await session.execute(query)
        result = res.scalars().all()
        return result
    except Exception as e:
        return HTTPException(status_code=500, detail=f"{e}")


@auth_router.get('/get_district/', response_model=List[district_list])
async def get_ditrict(region_id: int,
                      session: AsyncSession = Depends(get_async_session)
                      ):
    try:
        query = select(District).where(District.region_id == region_id)
        res = await session.execute(query)
        result = res.scalars().all()
        return result
    except Exception as e:
        return HTTPException(status_code=500, detail=f"{e}")


@auth_router.get("/student/user_info", response_model=UserData_info)
async def get_user_info(token: dict = Depends(verify_token),
                        session: AsyncSession = Depends(get_async_session)):
    try:
        user_id = token.get('user_id')
        query = select(User).where(User.id == user_id)
        res = await session.execute(query)
        result = res.scalar()
        return result
    except Exception as e:
        return HTTPException(status_code=400, detail=f"{e}")


@auth_router.get("/renter/user_info", response_model=RenterData_info)
async def get_user_info(token: dict = Depends(verify_token),
                        session: AsyncSession = Depends(get_async_session)):
    try:
        user_id = token.get('renter_id')
        query = select(Renter).where(Renter.id == user_id)
        res = await session.execute(query)
        result = res.scalar()
        return result
    except Exception as e:
        return HTTPException(status_code=400, detail=f"{e}")


@auth_router.put('/student/profile/update')
async def change_password_user(model:change_password,
                          token: dict = Depends(verify_token),
                          session: AsyncSession = Depends(get_async_session)
     ):
    try:
        if model.new_password==model.confirm_password:
            user_id = token.get('user_id')
            password_hash = pwd_context.hash(model.old_password)
            query = select(User).where(User.id==user_id)
            res = await session.execute(query)
            result = res.scalar()
            if result and pwd_context.verify(model.old_password, result.password):
                new_password_hash= pwd_context.hash(model.confirm_password)
                query_update = update(User).where(User.id==user_id).values(password=new_password_hash)
                await session.execute(query_update)
                await session.commit()
                return HTTPException(status_code=200,detail="Password changed")
            else:
                return HTTPException(status_code=400,detail="Old password is not correct")
        else:
            return HTTPException(status_code=400,detail="New passwords are not same")
    except Exception as e:
        return HTTPException(status_code=400,detail=f"{e}")


@auth_router.put('/renter/profile/update')
async def change_password_renter(model:change_password,
                          token: dict = Depends(verify_token),
                          session: AsyncSession = Depends(get_async_session)
     ):
    try:
        if model.new_password == model.confirm_password:
            user_id = token.get('renter_id')

            # Fetch the renter by user_id
            query = select(Renter).where(Renter.id == user_id)
            res = await session.execute(query)
            renter = res.scalar()

            if renter and pwd_context.verify(model.old_password, renter.password):
                new_password_hash = pwd_context.hash(model.confirm_password)
                query_update = update(Renter).where(Renter.id == user_id).values(password=new_password_hash)
                await session.execute(query_update)
                await session.commit()
                return {"detail": "Password changed successfully"}
            else:
                raise HTTPException(status_code=400, detail="Old password is not correct")
        else:
            raise HTTPException(status_code=400, detail="New passwords do not match")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))