from fastapi import FastAPI

from auth.auth import auth_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}




# app = FastAPI(title='User', version='1.0.0')

app.include_router(auth_router,prefix='/auth')

