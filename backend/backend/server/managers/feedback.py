from database import DB
from bson.objectid import ObjectId


class Feedback:
    collection = DB.get_collection('feedback_cfo')

    @staticmethod
    def helper(coroutine):
        result = {
            'login': coroutine['login'],
        }
        return

    def __init__(self, parameters: dict = None):

        if parameters:
            for key in parameters:
                self.__dict__[key] = parameters[key]

    def __setattr__(self, key, value):
        super().__setattr__(key, value)

    @classmethod
    async def get(cls, id):
        dictionary = await cls.collection.find_one({'_id': ObjectId(id)})

        if not dictionary:
            return None
        result = cls(parameters=dictionary)
        result._id = str(result._id)
        return result


    async def add(self):
        self.__dict__.update({'course_id': ObjectId(self.__dict__['course_id'])})
        await self.collection.insert_one(self.__dict__)


    async def update(self, parameters: dict):
        self.__dict__.update(parameters)
        self.__dict__.update({'_id': ObjectId(self.__dict__['_id'])})
        self.__dict__.update({'course_id': ObjectId(self.__dict__['course_id'])})
        await self.collection.update_one({'_id': self._id}, {'$set': self.__dict__})

    async def delete(self):
        self.__dict__.update({'_id': ObjectId(self.__dict__['_id'])})
        await self.collection.delete_one({'_id': self._id})

    async def response(self):
        data = self.__dict__
        return data

    @classmethod
    async def get_all(cls):
        results = []
        results_db = cls.collection.find({})
        async for result_db in results_db:
            res = cls(parameters=result_db)
            res._id = str(res._id)
            res.course_id = str(res.course_id)
            results.append(res)
        return results

    @classmethod
    async def get_feedbacks_course(cls, course_id):
        results = []
        results_db = cls.collection.find({'course_id': ObjectId(course_id)})
        async for result_db in results_db:
            res = cls(parameters=result_db)
            res._id = str(res._id)
            res.course_id = str(res.course_id)
            results.append(res)
        return results

