from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from auth.utils import verify_token
from database import get_async_session
from models.models import Rent, Renter
from renter.scheme import Rent_scheme, My_rent_scheme

renter_router = APIRouter()


@renter_router.post('/renter/add_rent')
async def add_rent(model: Rent_scheme,
                   token: dict = Depends(verify_token),
                   session: AsyncSession = Depends(get_async_session)
                   ):
    try:
        renter_id = token.get('renter_id')
        print(renter_id)
        query = insert(Rent).values(**dict(model), renter_id=renter_id)
        await session.execute(query)
        await session.commit()
        return HTTPException(status_code=200, detail="Rent added")
    except Exception as e:
        return HTTPException(status_code=400, detail=f"{e}")


@renter_router.get('/get_rents',response_model=List[My_rent_scheme])
async def get_rents(token: dict = Depends(verify_token),
                    session: AsyncSession = Depends(get_async_session)):
    try:
        renter_id = token.get('renter_id')
        query = select(Rent).where(Rent.renter_id == renter_id)
        res = await session.execute(query)
        result = res.scalars().all()
        list_rents = []
        if result:
            query_renter = select(Renter).where(Renter.id == renter_id)
            res_renter = await session.execute(query_renter)
            result_renter = res_renter.first()
            renter_dict = {
                'firstname': result_renter[0].firstname,
                'lastname': result_renter[0].lastname,
                'phone': result_renter[0].phone
            }
            for item in result:
                list_rents.append({
                    'id':item.id,
                    'name': item.name,
                    'description': item.description,
                    'room_count': item.room_count,
                    'total_price': item.total_price,
                    'student_jins_id': item.student_jins_id,
                    'renter_id': renter_dict,
                    'student_count': item.student_count,
                    'contract':item.contract,
                    'category_id': item.category_id,
                    'location': item.location,
                    'longitude': item.longitude,
                    'latitude': item.latitude,
                    'wifi': item.wifi,
                    'conditioner': item.conditioner,
                    'washing_machine': item.washing_machine,
                    'TV': item.TV,
                    'refrigerator': item.refrigerator,
                    'furniture': item.furniture,
                    'other_convenience': item.other_convenience
                })

                return list_rents
            else:
                return HTTPException(status_code=200, detail="You do not have any rents")


    except Exception as e:
        return HTTPException(status_code=400, detail=f"{e}")


