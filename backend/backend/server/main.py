from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from routers.user import user_router
from routers.avatars import avatar_router
from routers.feedback import router as feedback_router
from routers.course import router as course_router
from routers.models import router as model_router
from fastapi import FastAPI, Request
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from config import REDIS_NAME, REDIS_PORT, REDIS_HOST
import time
app = FastAPI()
app.include_router(user_router)
app.include_router(avatar_router)
app.include_router(course_router)
app.include_router(feedback_router)
app.include_router(model_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# for cache
@app.on_event('startup')
async def startup_event():
    redis = aioredis.from_url(F"{REDIS_NAME}://{REDIS_HOST}:{REDIS_PORT}", encoding='utf8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.get("/")
@cache(expire=600)
async def test():
    return 'success'


if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=9000)
