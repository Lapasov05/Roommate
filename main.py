from fastapi import FastAPI

from mobile.mobile import mobile_router

from auth.auth import auth_router
from models.models import User
from renter.renter import renter_router

app = FastAPI()
app.include_router(mobile_router)


app.include_router(mobile_router, prefix='/student')
app.include_router(auth_router, prefix='/auth')
app.include_router(renter_router, prefix='/renter')

