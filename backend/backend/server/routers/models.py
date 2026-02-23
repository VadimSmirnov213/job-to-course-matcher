from fastapi import APIRouter, Query, Depends, Body, Path, HTTPException, Query, status, Response
from typing import Annotated
from managers.user import User
from managers.course import Course
from fastapi import File, UploadFile
from fastapi.responses import FileResponse
from buckets.avatar import Avatar
from managers.user import User
from managers.vacs import Vacs
from managers.course import Course

from fastapi_cache.decorator import cache
from cel_que import get_dict, get_recommendations

router = APIRouter(prefix='/api/predict')


@router.get('/recommendation')
# @cache(expire=600)
async def recommendation(top: Annotated[int, Query()], url: Annotated[str, Query()]):
    vac = get_dict.delay(url).get()
    courses = await Course.get_all_for_predict()
    result = get_recommendations.delay(courses, vac, top).get()
    return result
