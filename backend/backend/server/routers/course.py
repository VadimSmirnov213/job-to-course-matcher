from fastapi import APIRouter, Depends, Body, Path, HTTPException, Query, status
from typing import Annotated
from managers.course import Course
from managers.feedback import Feedback
from schemas.course import CourseUpdate, CourseCreate

router = APIRouter(prefix='/api/courses')


@router.get('/{course_id}', status_code=200)
async def get_course(course_id: Annotated[str, Path()]):
    try:
        course = await Course.get(course_id)
        if not course:
            raise HTTPException(status_code=404, detail='Course with id not found')
        return course
    except:
        raise HTTPException(status_code=404, detail='Course id is invalid')




@router.post('', status_code=201)
async def create_course(schema: Annotated[CourseCreate, Body()]):
    parameters = schema.dict()

    try:
        course = Course(parameters=parameters)
        await course.add()
    except:
        raise HTTPException(status_code=400, detail='Course with id already registered')
    else:
        return 'OK'


@router.put('/{course_id}', status_code=200)
async def update_course(course_id: Annotated[str, Path()], schema: Annotated[CourseUpdate, Body()]):
    parameters = schema.dict()

    course = await Course.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail='Course with id not found')
    await course.update(parameters=parameters)
    return 'OK'


@router.delete('/{course_id}', status_code=200)
async def delete_course(course_id: Annotated[str, Path()]):
    course = await Course.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail='Course with id not found')
    await course.delete()
    return 'OK'


@router.get('', status_code=200)
async def get_all():
    courses = await Course.get_all()
    return courses

@router.get('/feedbacks/{course_id}')
async def get_feedbacks(course_id: Annotated[str, Path()]):
    try:
        course = await Course.get(course_id)
        if not course:
            raise HTTPException(status_code=404, detail='Course with id not found')
        feedbacks = await Feedback.get_feedbacks_course(course_id)
        return feedbacks
    except:
        raise HTTPException(status_code=404, detail='Course id is invalid')