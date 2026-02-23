from fastapi import APIRouter, Depends, Body, Path, HTTPException, Query, status, Response
from typing import Annotated
from managers.user import User

from fastapi import File, UploadFile
from fastapi.responses import FileResponse
from buckets.avatar import Avatar
from managers.user import User

avatar_router = APIRouter(prefix='/api/files/avatars')


@avatar_router.get('/{login}', status_code=200)
def get_avatar(login: Annotated[str, Path()]):
    file_content = Avatar.get(login)
    if not file_content:
        raise HTTPException(detail='avatar with login  not found', status_code=404)
    response = Response(content=file_content)
    response.headers["Content-Disposition"] = "attachment; filename=avatar.jpg"
    return response


@avatar_router.put("/{login}", status_code=200)
async def update_avatar(login: Annotated[str, Path()], file: UploadFile):
    user = await User.get(login)
    if not user:
        raise HTTPException(status_code=404, detail='User with login not found')
    avatar = Avatar(login, file)
    response = await avatar.load_to_storage()
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise HTTPException(status_code=500, detail='Storage error')
    return "Successfully update avatar"

@avatar_router.delete("/{login}")
async def delete_avatar(login: Annotated[str, Path()]):
    avatars = Avatar.all_keys()
    if not avatars or str(login) not in avatars:
        raise HTTPException(status_code=404, detail='avatar with login not found')
    response = Avatar.delete(login)
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise HTTPException(status_code=500, detail='Storage error')
    return 'Successfully delete avatar'
