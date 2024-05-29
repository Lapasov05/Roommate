from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import verify_stuff_token
from database import get_async_session
from models.models import User

stuff_router = APIRouter()

stuff_router.get('/admin/get_all/users')
async def get_all_users(token:dict=Depends(verify_stuff_token),
                        session:AsyncSession=Depends(get_async_session)):
    try:
        role_id = token.get('role_id')
        if role_id == 1:
            query = select(User)

    except Exception as e:
        return HTTPException(status_code=400,detail=str(e))