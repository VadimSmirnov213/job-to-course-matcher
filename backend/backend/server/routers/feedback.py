from fastapi import APIRouter, Depends, Body, Path, HTTPException, Query, status
from typing import Annotated
from managers.feedback import Feedback
from managers.course import Course
from schemas.feedback import FeedbackCreate
from schemas.feedback import FeedbackUpdate
router = APIRouter(prefix='/api/feedback')


@router.get('/{id}', status_code=200)
async def get_feedback(id: Annotated[str, Path()]):
    try:
        result = await Feedback.get(id)
    except:
        raise HTTPException(status_code=404, detail='Feedback id is invalid')
    if not result:
        raise HTTPException(status_code=404, detail='Feedback with id not found')
    return result


@router.post('', status_code=201)
async def create_feedback(schema: Annotated[FeedbackCreate, Body()]):
    parameters = schema.dict()
    try:
        course = await Course.get(schema.course_id)
    except:
        raise HTTPException(status_code=400, detail='Course id is invalid')
    if not course:
        raise HTTPException(status_code=404, detail='Course with id not found')
    await course.add_feedback(parameters)
    result = Feedback(parameters=parameters)
    await result.add()
    return 'OK'




@router.delete('/{id}', status_code=200)
async def delete_feedback(id: Annotated[str, Path()]):
    result = await Feedback.get(id)
    if not result:
        raise HTTPException(status_code=404, detail='Feedback with id not found')
    course = await Course.get(result['course_id'])
    await course.delete_feedback(result)
    if not course:
        raise HTTPException(status_code=404, detail='Course with id not found')
    await result.delete()
    return 'OK'


@router.get('', status_code=200)
async def get_all():
    result = await Feedback.get_all()
    return result
