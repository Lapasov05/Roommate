from typing import List

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import get_async_session
from mobile.scheme import RentGETScheme, RentADDScheme, FilterScheme
from models.models import Rent

mobile_router = APIRouter()


@mobile_router.get('/mobile')
async def say_hello(

):
    return "Hello world"


@mobile_router.get('/rent', response_model=List[RentGETScheme])
async def get_all_rent(
    session: AsyncSession = Depends(get_async_session)
):
    query = select(Rent).options(selectinload(Rent.jins), selectinload(Rent.category))
    rent = await session.execute(query)
    print(rent)
    rent_data = rent.scalars().all()
    return rent_data


@mobile_router.post('/add-rent')
async def add_rent(
        data: RentADDScheme,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        await session.execute(insert(Rent).values(**data.dict()))
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail='Error inserting request')

    return {'success': True}


# Filters

@mobile_router.get('/filters')
async def rent_filter(
        data: FilterScheme,
        session: AsyncSession = Depends(get_async_session)
):
    pass












