from fastapi import APIRouter, Depends, Body, Path, HTTPException, Query, status
from typing import Annotated
from managers.user import User
from schemas.user import UserLogin, UserResponse
from schemas.user import UserCreate
user_router = APIRouter(prefix='/api/users')


@user_router.get('/{login}', status_code=200)
async def get_user(login: Annotated[str, Path()]):
    user = await User.get(login)
    if not user:
        raise HTTPException(status_code=404, detail='User with login not found')
    data = await user.response()
    return data


@user_router.post('', status_code=201)
async def create_user(login: Annotated[str, Body()], password: Annotated[str, Body()],
                      schema: Annotated[UserCreate, Body()]

                      ):
    parameters = schema.dict()
    parameters.update({'password': password})

    try:
        user = User(login=login, parameters=parameters)
        await user.add()
    except:
        raise HTTPException(status_code=400, detail='User with login already registered')
    else:
        return 'OK'


@user_router.put('/{login}', status_code=200)
async def update_user(login: Annotated[str, Path()], schema: Annotated[UserCreate, Body()]):
    parameters = schema.dict()
    if 'login' in parameters:
        raise HTTPException(status_code=400, detail='Field login is immutable')
    user = await User.get(login=login)
    if not user:
        raise HTTPException(status_code=404, detail='User with login not found')
    await user.update(parameters=parameters)
    return 'OK'


@user_router.delete('/{login}', status_code=200)
async def delete_user(login: Annotated[str, Path()]):
    user = await User.get(login=login)
    if not user:
        raise HTTPException(status_code=404, detail='User with login not found')
    await user.delete()
    return 'OK'


@user_router.post('/login', status_code=200)
async def login_user(login: Annotated[str, Body()], password: Annotated[str, Body()]):
    user = await User.login(login, password)
    if not user:
        raise HTTPException(status_code=401, detail='Incorrect login or password')
    return 'Success login'