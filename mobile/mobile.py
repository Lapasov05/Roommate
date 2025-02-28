import datetime
import secrets
from typing import List

import aiofiles
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi_pagination import Page, add_pagination, paginate
# from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy import select, insert, or_, and_, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from auth.utils import verify_token
from database import get_async_session
from mobile.scheme import RentGETScheme, RentADDScheme, FilterScheme, ReviewPostScheme, RateGetScheme, \
    WishlistGETScheme, AnnouncementPOSTScheme, FacultyCreate, UniversityCreate
from models.models import Rent, Image, Rate, Wishlist, University, Faculty

from datetime import datetime, timedelta

mobile_router = APIRouter()


# @mobile_router.get('/rent')
# async def get_all_rent(
#         page: int = 1,
#         size: int = 10,
#         token: dict = Depends(verify_token),
#         session: AsyncSession = Depends(get_async_session)
# ) -> Page[RentGETScheme]:
#     try:
#         gender_id = token['jins_id']
#         query = select(Rent).options(
#             selectinload(Rent.jins),
#             selectinload(Rent.category),
#             selectinload(Rent.renter),
#             selectinload(Rent.image)
#         ).where(Rent.student_jins_id == gender_id)
#         rent = await session.execute(query)
#         rent_data = rent.scalars().all()
#         return paginate(rent_data)
#     except Exception as e:
#         raise HTTPException(status_code=401, detail="Not authenticated")

# add_pagination(mobile_router)


@mobile_router.get('/rent_by_id', response_model=RentGETScheme, tags=['Renter'])
async def get_all_rent_by_id(
        rent_id: int,
        token: dict = Depends(verify_token),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        gender_id = token['jins_id']
        if gender_id is None:
            raise HTTPException(status_code=404, detail='Not authenticated')
        data = await session.execute(select(Rent).options(
            selectinload(Rent.renter), selectinload(Rent.jins), selectinload(Rent.category)).where(
            and_(Rent.id == rent_id, Rent.student_jins_id == token['jins_id'])
        ))
        return data.scalars().one_or_none()
    except Exception as e:
        raise HTTPException(status_code=401, detail='Not authenticated')


@mobile_router.post('/add-rent', tags=['Renter'])
async def add_rent(
        data: RentADDScheme,
        token: dict = Depends(verify_token),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        renter_id = token['renter_id']
        await session.execute(insert(Rent).values(**data.dict(), renter_id=renter_id))
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail='Error inserting request')

    return {'success': True}


@mobile_router.get('/home/filters-news', tags=['Home'])
async def rent_filter(
        token: dict = Depends(verify_token),
        session: AsyncSession = Depends(get_async_session)
):
    jins_id = token.get('jins_id')
    three_days_ago = datetime.now() - timedelta(days=3)

    rents = select(Rent).options(
        selectinload(Rent.jins),
        selectinload(Rent.category),
        selectinload(Rent.renter)
    ).where(
        Rent.created_at >= three_days_ago
        , Rent.student_jins_id == jins_id
    )

    # Execute the query
    result = await session.execute(rents)
    rented_items = result.scalars().all()

    return rented_items


@mobile_router.post('/add-image-rent', tags=['Renter'])
async def add_image_rent(
        image: UploadFile,
        rent_id: int,
        token: dict = Depends(verify_token),
        session: AsyncSession = Depends(get_async_session)
):
    url = f'images/{image.filename}'
    async with aiofiles.open(url, 'wb') as zipf:
        content = await image.read()
        await zipf.write(content)
    hashcode = secrets.token_hex(32)
    data = insert(Image).values(url=url, hashcode=hashcode, rent_id=rent_id)
    await session.execute(data)
    await session.commit()
    return {'success': True}


@mobile_router.get('/image', response_class=FileResponse, tags=['Home'])
async def get_image(
        hashcode: str,
        token: dict = Depends(verify_token),
        session: AsyncSession = Depends(get_async_session)
):
    data = await session.execute(select(Image).where(Image.hashcode == hashcode))
    image = data.scalars().first()
    if image:
        some_file_path = f"{image.url}"
        return some_file_path
    else:
        raise HTTPException(status_code=400, detail='Image is not available!')


@mobile_router.post('/add-review', tags=['Home'])
async def add_review(
        review_data: ReviewPostScheme,
        token: dict = Depends(verify_token),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        await session.execute(
            insert(Rate).values(
                **review_data.dict(), user_id=token['user_id'])
        )
        await session.commit()
        return {'review_data': review_data}
    except HTTPException as e:
        raise HTTPException(status_code=400, detail="Bad request!!!")


@mobile_router.get('/get_rents/get-review', response_model=List[RateGetScheme], tags=['Renter'])
async def get_rents_review(
        rent_id: int,
        token: dict = Depends(verify_token),
        session: AsyncSession = Depends(get_async_session)
):
    query = select(Rate).options(selectinload(Rate.user)).where(Rate.rent_id == rent_id)
    data = await session.execute(query)
    rate_data = data.scalars().all()
    return rate_data


@mobile_router.post('/add-wishlist', tags=['Wishlist'])
async def add_wishlist(
    rent_id: int,
    token: dict = Depends(verify_token),
    session: AsyncSession = Depends(get_async_session)
):
    user_id = token['user_id']
    wishlist_data = await session.execute(
        select(Wishlist).options(selectinload(Wishlist.rent), selectinload(Wishlist.user)).where(
            and_(Wishlist.rent_id == rent_id, Wishlist.user_id == user_id)
        ))
    wish_data = wishlist_data.scalars().one_or_none()
    if wish_data:
        await session.execute(delete(Wishlist).where(and_(Wishlist.rent_id==rent_id, Wishlist.user_id==user_id)))
    else:
        await session.execute(insert(Wishlist).values(user_id=user_id, rent_id=rent_id))
    await session.commit()
    return {'success': True}


@mobile_router.get('/get-wishlist', response_model=List[WishlistGETScheme], tags=['Wishlist'])
async def get_wishlist(
        token: dict = Depends(verify_token),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(Wishlist).options(selectinload(Wishlist.rent)).where(Wishlist.user_id == token['user_id'])
        data = await session.execute(query)
        return data
    except NoResultFound:
        raise HTTPException(status_code=404, detail='Wishlist is not available!')


@mobile_router.get('/search-rents', tags=['Renter'])
async def get_all_rents(
        query: str,
        token: dict = Depends(verify_token),
        session: AsyncSession = Depends(get_async_session)
) -> Page[RentGETScheme]:
    gender = token.get('jins_id')
    search_query = f'%{query}%'
    query_data = select(Rent).options(
        selectinload(Rent.jins),
        selectinload(Rent.category),
        selectinload(Rent.renter)
    ).where(and_(Rent.student_jins_id == gender, or_(Rent.name.ilike(search_query), Rent.description.ilike(search_query))))
    data = await session.execute(query_data)
    return paginate(data.scalars().all())

# add_pagination(mobile_router)


@mobile_router.get('/add-announcement', tags=['Home'])
async def add_announcement(
        data: AnnouncementPOSTScheme,
        token: dict = Depends(verify_token),
        session: AsyncSession = Depends(get_async_session)
):
    user_id = token['user_id']




#===============================================================


@mobile_router.post("/universities",tags=['Sarvinoz'])
async def create_university(
    university: UniversityCreate,
    session: AsyncSession = Depends(get_async_session)
):
    db_university = University(**university.dict())
    session.add(db_university)
    await session.commit()
    await session.refresh(db_university)
    return db_university


@mobile_router.post("/faculties",tags=['Sarvinoz'])
async def create_faculty(
    faculty: FacultyCreate,
    session: AsyncSession = Depends(get_async_session)
):
    db_faculty = Faculty(**faculty.dict())
    session.add(db_faculty)
    await session.commit()
    await session.refresh(db_faculty)
    return db_faculty

