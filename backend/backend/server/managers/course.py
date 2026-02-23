from database import DB
from bson.objectid import ObjectId


class Course:
    collection = DB.get_collection('courses_cfo')

    def helper(self):
        response = self.__dict__
        response['_id'] = str(response['_id'])
        return

    def __init__(self, parameters: dict = None):

        if parameters:
            for key in parameters:
                self.__dict__[key] = parameters[key]

    def __setattr__(self, key, value):
        super().__setattr__(key, value)

    @classmethod
    async def get(cls, id):
        course_dict = await cls.collection.find_one({'_id': ObjectId(id)})

        if not course_dict:
            return None
        course = cls(parameters=course_dict)
        course._id = str(course._id)
        return course

    async def add(self):
        await self.collection.insert_one(self.__dict__)

    async def update(self, parameters: dict):
        self.__dict__.update(parameters)
        self.__dict__.update({'_id': ObjectId(self.__dict__['_id'])})
        await self.collection.update_one({'_id': self._id}, {'$set': self.__dict__})

    async def delete(self):
        self.__dict__.update({'_id': ObjectId(self.__dict__['_id'])})
        await self.collection.delete_one({'_id': self._id})

    async def response(self):
        data = self.__dict__
        return data

    async def add_feedback(self, feedback: dict):
        rating = self.rating
        count_views = self.count_views
        numerator = rating * count_views + feedback['count_star']
        denominator = count_views + 1
        self.rating = numerator / denominator
        self.count_views = count_views + 1
        self.__dict__.update({'_id': ObjectId(self.__dict__['_id'])})
        await self.collection.update_one({'_id': self._id}, {'$set': self.__dict__})

    async def delete_feedback(self, feedback):
        rating = self.rating
        count_views = self.count_views
        numerator = rating * count_views + feedback['count_star']
        denominator = count_views - 1
        self.rating = numerator / denominator
        self.count_views = count_views - 1
        self.__dict__.update({'_id': ObjectId(self.__dict__['_id'])})
        await self.collection.update_one({'_id': self._id}, {'$set': self.__dict__})

    @classmethod
    async def get_all(cls):
        courses = []
        courses_db = cls.collection.find({})
        async for course_db in courses_db:
            course = cls(parameters=course_db)
            course._id = str(course._id)
            courses.append(course)

        return courses

    @classmethod
    async def get_all_for_predict(cls):
        courses = []
        courses_db = cls.collection.find({})
        async for course_db in courses_db:
            course = course_db
            course['_id'] = str(course['_id'])
            # del course['_id']
            courses.append(course)

        return courses
